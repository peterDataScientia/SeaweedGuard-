library(OpenSpecy)
args <- commandArgs(trailingOnly=TRUE)
root <- args[1]
out <- file.path(root,"06_OpenSpecy")
dir.create(out,recursive=TRUE,showWarnings=FALSE)
writeLines(capture.output(sessionInfo()),file.path(out,"session_info.txt"))
options(timeout=1800)
raw_lib <- tryCatch(load_lib(type="derivative"),error=function(e) NULL)
if (is.null(raw_lib)) {
  get_lib(type="derivative")
  raw_lib <- load_lib(type="derivative")
}
writeLines(capture.output(str(raw_lib,max.level=2,list.len=20)),file.path(out,"library_structure.txt"))
if (inherits(raw_lib,"OpenSpecy") && !is.null(raw_lib$metadata)) {
  lib <- raw_lib
  ftir_only <- FALSE
} else {
  keys <- names(raw_lib)
  idx <- grep("^(ftir|ir|infrared)$",keys,ignore.case=TRUE)
  if (length(idx)!=1L) stop("Cannot identify FTIR library; inspect library_structure.txt")
  lib <- raw_lib[[idx]]
  ftir_only <- TRUE
}
if (is.null(lib$metadata)) stop("Selected reference object has no metadata; inspect library_structure.txt")
meta <- as.data.frame(lib$metadata)
stopifnot(nrow(meta)>0,ncol(meta)>0)
if (!"SpectrumType" %in% names(meta)) {
  if (!ftir_only) stop("Missing SpectrumType in combined library")
  meta$SpectrumType <- "FTIR"
}
write.csv(meta,file.path(out,"reference_metadata.csv"),row.names=FALSE)
message("Reference metadata exported: ",nrow(meta)," rows")
print(table(meta$SpectrumType,useNA="ifany"))
# Metadata review is mandatory before selecting a provenance-clean reference pool.
review <- file.path(out,"reference_review_audited.csv")
if (!file.exists(review)) stop("Audited review missing")
r <- read.csv(review,stringsAsFactors=FALSE)
stopifnot(nrow(r)==nrow(meta),identical(as.integer(r$index),seq_len(nrow(meta))),
          identical(as.character(r$sample_name),as.character(meta$sample_name)))
keep <- which(tolower(as.character(r$include))=="true")
stopifnot(length(keep)==459L,all(meta$organization[keep] %in% c("flopp, de frond et al. 2021","primpke et al. 2018")))
approved <- meta[keep,,drop=FALSE]
lib <- filter_spec(lib,logic=as.character(approved$sample_name))
stopifnot(nrow(lib$metadata)==length(keep),setequal(as.character(lib$metadata$sample_name),as.character(approved$sample_name)))
write.csv(approved,file.path(out,"approved_reference_metadata.csv"),row.names=FALSE)
message("Approved references: ",length(keep))
input <- file.path(out,"queries")
files <- list.files(input,pattern="\\.csv$",full.names=TRUE)
truth <- read.csv(file.path(out,"truth.csv"),stringsAsFactors=FALSE)
stopifnot(length(files)==232L,setequal(sub("\\.csv$","",basename(files)),truth$hash))
results <- list()
for (f in files) {
  a <- read.csv(f)
  q <- as_OpenSpecy(x=a$wavenumber,spectra=data.frame(query=a$absorbance))
  q <- process_spec(q,conform_spec=FALSE,smooth_intens=TRUE,smooth_intens_args=list(polynomial=3,window=11,derivative=1,abs=TRUE))
  m <- match_spec(q,library=lib,conform=TRUE,top_n=5)
  m <- as.data.frame(m)
  stopifnot(all(c("library_id","match_val") %in% names(m)),nrow(m)>0)
  pos <- match(as.character(m$library_id),as.character(lib$metadata$sample_name))
  stopifnot(!anyNA(pos))
  for (col in intersect(c("spectrum_identity","material_class","material","sample_name","organization"),names(lib$metadata))) {
    m[[col]] <- lib$metadata[[col]][pos]
  }
  m$query_id <- sub("\\.csv$","",basename(f))
  results[[length(results)+1]] <- m
  write.csv(do.call(rbind,results),file.path(out,"matches_partial.csv"),row.names=FALSE)
}
write.csv(do.call(rbind,results),file.path(out,"matches.csv"),row.names=FALSE)
