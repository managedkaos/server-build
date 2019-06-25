#!/usr/bin/Rscript
installer <- function(pkg) {
    if (nzchar(system.file(package = pkg))) {
        message('Already installed:', pkg)
    } else {
        install.packages(pkg)
    }
}

installer("rJava")
installer("data.table")
installer('NLP')
installer('SnowballC')
installer('dplyr')
installer('ggplot2')
installer('googleLanguageR')
installer('httr')
installer('imager')
installer('jsonlite')
installer('openNLP')
installer('qdap')
installer('rdrop2')
installer('tidytext')
installer('tidyverse')
installer('tm')
installer('tokenizers')
installer('zoo')
install.packages("RDRPOSTagger", repos = "http://www.datatailor.be/rcube", type = "source")
