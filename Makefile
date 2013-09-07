.PHONY: all clean
.INTERMEDIATE: %.fna.gz %.fna %.aln %.phy

all: data trees

clean:
	rm -f data/*.pkl data/*.fna data/*.aln data/*.aln2 data/*.phy
	rm -f RAxML*

download: list $(patsubst %, data/%.fna.gz, $(shell python scripts/metagenome_list.py data/metagenome_list.pkl))

trees: list data/metagenome_list.pkl $(patsubst %, data/%.new, $(shell python scripts/metagenome_list.py data/metagenome_list.pkl))

list: data data/metagenome_list.pkl

data:
	mkdir data

data/metagenome_list.pkl: scripts/get_metagenome_list.py
	python $< $@

data/%.fna.gz: data/metagenome_list.pkl scripts/download_metagenomes.py
	python scripts/download_metagenomes.py $< data/ $(shell python -c "print '$@'[len('data/'):-len('.fna.gz')]")

%.fna: %.fna.gz
	gunzip -c $< | python scripts/subsample_sequences.py 100 > $@

%.aln: %.fna
	muscle -in $< -out $@

%.phy: %.aln scripts/guid_labels.py
	cat $< | python scripts/guid_labels.py | \
	python -c "import Bio.AlignIO as aio; import sys; aio.convert(sys.stdin,'fasta','$@','phylip')"

%.new: %.phy
	rm -f RAxML*
	raxmlHPC -m GTRCAT -n $(shell python -c "print '$@'.split('/')[-1][:-len('.new')]") -p 10000 -s $<
	mv RAxML_result.$(shell python -c "print '$@'.split('/')[-1][:-len('.new')]") $@
	rm -f RAxML*
