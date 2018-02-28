#!/usr/bin/env python
#Dan Blankenberg
import sys
import optparse

from pyBamParser.bam import Reader
from pyBamTools.genotyping.naive import VCFReadGroupGenotyper, PROGRAM_NAME, PROGRAM_VERSION

def main():
    #Parse Command Line
    parser = optparse.OptionParser()
    parser.add_option( '-b', '--bam', dest='bam_file', action='append', type="string", default=[], help='BAM filename, optionally index filename. Multiple allowed.' )
    parser.add_option( '-i', '--index', dest='index_file', action='append', type="string", default=[], help='optionally index filename. Multiple allowed.' )
    parser.add_option( '-o', '--output_vcf_filename', dest='output_vcf_filename', action='store', default = None, type="string", help='Output VCF filename' )
    parser.add_option( '-r', '--reference_genome_filename', dest='reference_genome_filename', action='store', default = None, type="string", help='Input reference file' )
    parser.add_option( '-v', '--variants_only', dest='variants_only', action='store_true', default = False, help='Report only sites with a possible variant allele.' )
    parser.add_option( '-s', '--use_strand', dest='use_strand', action='store_true', default = False, help='Report counts by strand' )
    parser.add_option( '-p', '--ploidy', dest='ploidy', action='store', type="int", default=2, help='Ploidy. Default=2.' )
    parser.add_option( '-d', '--min_support_depth', dest='min_support_depth', action='store', type="int", default=0, help='Minimum number of reads needed to consider a REF/ALT. Default=0.' )
    parser.add_option( '-q', '--min_base_quality', dest='min_base_quality', action='store', type="int", default=None, help='Minimum base quality.' )
    parser.add_option( '-m', '--min_mapping_quality', dest='min_mapping_quality', action='store', type="int", default=None, help='Minimum mapping.' )
    parser.add_option( '-t', '--coverage_dtype', dest='coverage_dtype', action='store', type="string", default=None, help='dtype to use for coverage array' )
    parser.add_option( '--allow_out_of_bounds_positions', dest='allow_out_of_bounds_positions', action='store_true', default = False, help='Allows out of bounds positions to not throw fatal errors' )
    parser.add_option( '--safe', dest='safe', action='store_true', default = False, help='Perform checks to prevent certain errors. Is slower.' )
    parser.add_option( '--region', dest='region', action='append', type="string", default=[], help='region. Either <chrom> or <chrom>:<start>-<end>, origin-0 half-open.' )
    parser.add_option( '--regions_filename', dest='regions_file', action='append', type="string", default=[], help='Regions filename. Three columns, origin-0 half-open. Extra columns ignored. Multiple allowed.' )
    parser.add_option( '--regions_file_columns', dest='regions_file_columns', action='append', type="string", default=[], help='Columns in regions file for chrom,start,end. 0-based' )
    parser.add_option( '', '--version', dest='version', action='store_true', default = False, help='Report version and quit' )
    (options, args) = parser.parse_args()
    
    if options.version:
        print "%s version %s" % ( PROGRAM_NAME, PROGRAM_VERSION )
        sys.exit(0)
    
    if len( options.bam_file ) == 0:
        print >>sys.stderr, 'You must provide at least one bam (-b) file.'
        parser.print_help( sys.stderr )
        sys.exit( 1 )
    if options.index_file:
        assert len( options.index_file ) == len( options.bam_file ), "If you provide a name for an index file, you must provide the index name for all bam files."
        bam_files = zip( options.bam_file, options.index_file )
    else:
        bam_files = [ ( x, ) for x in options.bam_file ]
    if not options.reference_genome_filename:
        print >> sys.stderr, "Warning: Reference file has not been specified. Providing a reference genome is highly recommended."
    if options.output_vcf_filename:
        out = open( options.output_vcf_filename, 'wb' )
    else:
        out = sys.stdout
    
    regions = []
    if options.region:
        for region in options.region:
            region_split = region.split( ":" )
            region = region_split.pop( 0 )
            if region_split:
                region_split = filter( bool, region_split[0].split( '-' ) )
                if region_split:
                    if len( region_split ) != 2:
                        print >> sys.stderr, "You must specify both a start and an end, or only a chromosome when specifying regions."
                        sys.exit( 1 )
                    region = tuple( [ region ] + map( int, region_split ) )
            regions.append( region )
    
    if options.regions_file:
        if options.regions_file_columns:
            if len( options.regions_file_columns ) != len( options.regions_file ):
                print >> sys.stderr, "If you are providing columns for one regions file, you must provide columns for all regions files."
                sys.exit( 1 )
        else:
            options.regions_file_columns = ['0,1,2'] * len( options.regions_file )
        for regions_filename, regions_columns in zip( options.regions_file, options.regions_file_columns ):
            cols = map( int, regions_columns.split( ',' ) )
            if len( cols ) != 3:
                print >> sys.stderr, "You must specify chromosome, start, and end when specifying region columns."
                sys.exit( 1 )
            col_max = max( cols )
            with open( regions_filename, 'rt' ) as f:
                for region in f:
                    region_split = region.split( '\t' )
                    if len( region_split ) < col_max + 1:
                        print >> sys.stderr, "You must provide chromosome, start, and end when specifying regions from a file."
                        sys.exit( 1 )
                    regions.append( ( region_split[ cols[0] ], int( region_split[ cols[1] ] ), int( region_split[ cols[2] ] ) ) )
    
    coverage = VCFReadGroupGenotyper( map( lambda x: Reader( *x ), bam_files ), options.reference_genome_filename, dtype=options.coverage_dtype,
                                               min_support_depth=options.min_support_depth, min_base_quality=options.min_base_quality, 
                                               min_mapping_quality=options.min_mapping_quality, restrict_regions=regions, use_strand=options.use_strand, 
                                               allow_out_of_bounds_positions=options.allow_out_of_bounds_positions, safe=options.safe )
    for line in coverage.iter_vcf( ploidy=options.ploidy, variants_only=options.variants_only ):
        out.write( "%s\n" % line )
    out.close()

if __name__ == "__main__": main()
