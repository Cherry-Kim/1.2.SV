import string,sys,os,glob

## Germline SV calling
#os.system('/home/program/delly_v0.8.3_linux_x86_64bit call -x /home/program/delly/excludeTemplates/human.hg19.excl.tsv -o delly.bcf -g /home/DATA/EYE/hg19.fa RB1_RO_W40_N_dedup.bam')
#os.system('bcftools view del.bcf > delly.vcf')

PATH='/home/hykim/SV/delly/'
file_list=os.listdir(PATH)
bam_list= [file for file in file_list if file.endswith("_dedup.bam")]

#STEP1. SV calling is done by sample
for i in bam_list:
	sample=i.split('_dedup.bam')[0]
	os.system('/home/program/delly_v0.8.3_linux_x86_64bit call -g /home/hykim/REF/Human/hg19/hg19.fa -o '+sample+'.bcf -x /home/program/delly/excludeTemplates/human.hg19.excl.tsv '+i)

print "STEP2. Merge SV sites into a unified site list"
bcf_list= [file for file in file_list if file.endswith(".bcf")]
print bcf_list
os.system('/home/program/delly_v0.8.3_linux_x86_64bit merge -o sites.bcf '+" ".join(bcf_list))
os.system('bcftools view sites.bcf > sites.vcf')

print "STEP3. Genotype this merged SV site list across all samples."
for i in bam_list:
	sample=i.split('_dedup.bam')[0]
	os.system('/home/program/delly_v0.8.3_linux_x86_64bit call -g /home/hykim/REF/Human/hg19/hg19.fa -v sites.bcf -o '+sample+'.geno.bcf -x /home/program/delly/excludeTemplates/human.hg19.excl.tsv '+i)
	os.system('bcftools view '+sample+'.bcf > '+sample+'sites.vcf')

print "STEP4. Merge all genotyped samples to get a single VCF/BCF using bcftools merge"
geno_list= [file for file in file_list if file.endswith(".geno.bcf")]
os.system('bcftools merge -m id -O b -o merged.bcf '+" ".join(geno_list))
os.system('bcftools index merged.bcf')
#os.system('bcftools view merged.bcf > merged.vcf')

print "STEP5. Apply the germline SV filter which requires at least 20 unrelated samples"
os.system('/home/program/delly_v0.8.3_linux_x86_64bit filter -f germline -o germline.bcf merged.bcf')
os.system('bcftools view germline.bcf > germline.vcf')
