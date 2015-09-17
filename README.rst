This repository contains the **Naive Variant Caller** tool.

------

**What it does**

This tool is a naive variant caller that processes aligned sequencing reads from the BAM format and produces a VCF file containing per position variant calls. This tool allows multiple BAM files to be provided as input and utilizes read group information to make calls for individual samples. 

User configurable options allow filtering reads that do not pass mapping or base quality thresholds and minimum per base read depth; user's can also specify the ploidy and whether to consider each strand separately. 

In addition to calling alternate alleles based upon simple ratios of nucleotides at a position, per base nucleotide counts are also provided. A custom tag, NC, is used within the Genotype fields. The NC field is a comma-separated listing of nucleotide counts in the form of <nucleotide>=<count>, where a plus or minus character is prepended to indicate strand, if the strandedness option was specified.
 

------

**Inputs**

Accepts one or more BAM input files and a reference genome from the built-in list or from a FASTA file in your history.


**Outputs**

The output is in VCF format.

Example VCF output line, without reporting by strand:
    ``chrM	16029	.	T	G,A,C	.	.	AC=15,9,5;AF=0.00155311658729,0.000931869952371,0.000517705529095	GT:AC:AF:NC	0/0:15,9,5:0.00155311658729,0.000931869952371,0.000517705529095:A=9,C=5,T=9629,G=15,``

Example VCF output line, when reporting by strand:
    ``chrM	16029	.	T	G,A,C	.	.	AC=15,9,5;AF=0.00155311658729,0.000931869952371,0.000517705529095	GT:AC:AF:NC	0/0:15,9,5:0.00155311658729,0.000931869952371,0.000517705529095:+T=3972,-A=9,-C=5,-T=5657,-G=15,``

**Options**

Reference Genome:

    Ensure that you have selected the correct reference genome, either from the list of built-in genomes or by selecting the corresponding FASTA file from your history.

Restrict to regions:

    You can specify any number of regions on which you would like to receive results. You can specify just a chromosome name, or a chromosome name and start postion, or a chromosome name and start and end position for the set of desired regions. 

Minimum number of reads needed to consider a REF/ALT:

    This value declares the minimum number of reads containing a particular base at each position in order to list and use said allele in genotyping calls. Default is 0.

Minimum base quality:

    The minimum base quality score needed for the position in a read to be used for nucleotide counts and genotyping. Default is no filter.

Minimum mapping quality:

    The minimum mapping quality score needed to consider a read for nucleotide counts and genotyping. Default is no filter.

Ploidy:

    The number of genotype calls to make at each reported position.

Only write out positions with possible alternate alleles:

    When set, only positions which have at least one non-reference nucleotide which passes declare filters will be present in the output.

Report counts by strand:

    When set, nucleotide counts (NC) will be reported in reference to the aligned read's source strand. Reported as: <strand><BASE>=<COUNT>.

Choose the dtype to use for storing coverage information:

    This controls the maximum depth value for each nucleotide/position/strand (when specified). Smaller values require the least amount of memory, but have smaller maximal limits.

        +--------+----------------------------+
        | name   | maximum coverage value     |
        +========+============================+
        | uint8  | 255                        |
        +--------+----------------------------+
        | uint16 | 65,535                     |
        +--------+----------------------------+
        | uint32 | 4,294,967,295              |
        +--------+----------------------------+
        | uint64 | 18,446,744,073,709,551,615 |
        +--------+----------------------------+


------

**Citation**

If you use this tool, please cite Blankenberg D, et al. *In preparation.*
