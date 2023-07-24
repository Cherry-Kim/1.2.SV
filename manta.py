import string,sys,os,glob
  
def STEP1_Configuration(REFERENCE_GENOME,bam_list,path):
    os.system('configManta.py '+' '.join(map(lambda z:'--bam '+path+z, bam_list))+' --referenceFasta '+REFERENCE_GENOME+' --runDir output_directory')

def STEP2_manta():
    os.chdir('output_directory/')
    os.system('./runWorkflow.py -m local -j 48')

def main():
    path, REFERENCE_GENOME = '/WES/2.bam/', 'REF/GRCh38_DNA/GRCh38.primary_assembly.genome.fa'
    file_list = os.listdir(path)
    bam_list = [file for file in file_list if file.endswith('.sort.bam')]
    bam_list.sort()
    STEP1_Configuration(REFERENCE_GENOME,bam_list,path)
    STEP2_manta()
main()
