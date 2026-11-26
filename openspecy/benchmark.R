library(OpenSpecy)
args <- commandArgs(trailingOnly=TRUE)
root <- args[1]
out <- file.path(root,"06_OpenSpecy")
dir.create(out,recursive=TRUE,showWarnings=FALSE)
writeLines(capture.output(sessionInfo()),file.path(out,"session_info.txt"))
get_lib(type="derivative")
lib <- load_lib(type="derivative")
meta <- as.data.frame(lib$metadata)
write.csv(meta,file.path(out,"reference_metadata.csv"),row.names=FALSE)
stopifnot("SpectrumType" %in% names(meta))
print(table(meta$SpectrumType,useNA="ifany"))
# Metadata review is mandatory before selecting a provenance-clean reference pool.
review <- file.path(out,"reference_review.csv")
if (!file.exists(review)) {
  write.csv(data.frame(index=seq_len(nrow(meta)),include=FALSE,reason="pending provenance review"),review,row.names=FALSE)
  stop("Review reference_metadata.csv and reference_review.csv before matching. Include only verified FTIR references unrelated to the test collection.")
}
r <- read.csv(review)
stopifnot(nrow(r)==nrow(meta),identical(as.integer(r$index),seq_len(nrow(meta))))
keep <- which(r$include %in% c(TRUE,"TRUE","true") & grepl("FTIR|infrared|^IR$",meta$SpectrumType,ignore.case=TRUE))
stopifnot(length(keep)>0)
lib <- filter_spec(lib,keep)
input <- file.path(out,"queries")
files <- list.files(input,pattern="\\.csv$",full.names=TRUE)
stopifnot(length(files)>0)
results <- list()
for (f in files) {
  a <- read.csv(f)
  q <- as_OpenSpecy(x=a$wavenumber,spectra=data.frame(query=a$absorbance))
  q <- process_spec(q,conform_spec=FALSE,smooth_intens=TRUE)
  m <- match_spec(q,library=lib,conform=TRUE,top_n=5)
  m <- as.data.frame(m)
  for (col in intersect(c("SpectrumIdentity","polymer_class","sample_name","organization"),names(lib$metadata))) {
    # Preserve native match identifiers and use package metadata accessor.
    m[[col]] <- vapply(m$library_id,function(id) {
      v <- get_metadata(lib,logic=id,rm_empty=FALSE)[[col]]
      if(length(v)==1) as.character(v) else NA_character_
    },character(1))
  }
  m$query_id <- sub("\\.csv$","",basename(f))
  results[[length(results)+1]] <- m
  write.csv(do.call(rbind,results),file.path(out,"matches_partial.csv"),row.names=FALSE)
}
write.csv(do.call(rbind,results),file.path(out,"matches.csv"),row.names=FALSE)
