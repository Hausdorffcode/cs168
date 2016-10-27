P = project3

all:	$P.pdf 

%.pdf: %.tex
	pdflatex $<

clean:
	$(RM) $P.log $P.aux $P.bbl $P.blg $P.out $P.dvi $P.ps $P.ps.gz *.pdf texput.log  *.tex~ $P.run.xml $P.bcf
