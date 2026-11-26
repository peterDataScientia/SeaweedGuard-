# Source only after benchmark.R has populated approved, out, truth and files.
# Raw reference spectra must be identified by stable sample IDs.
raw <- tryCatch(load_lib(type="raw"),error=function(e) NULL)
if(is.null(raw)) {
  get_lib(type="raw")
  raw <- load_lib(type="raw")
}
if (!inherits(raw,"OpenSpecy") || is.null(raw$metadata)) {
  ix <- grep("^(ftir|ir|infrared)$",names(raw),ignore.case=TRUE)
  stopifnot(length(ix)==1L)
  raw <- raw[[ix]]
}
ids <- as.character(approved$sample_name)
stopifnot(!anyDuplicated(ids),all(ids %in% as.character(raw$metadata$sample_name)))
raw <- filter_spec(raw,logic=ids)
stopifnot(nrow(raw$metadata)==459L,setequal(ids,as.character(raw$metadata$sample_name)))
sp <- as.matrix(raw$spectra)
stopifnot(nrow(sp)==length(raw$wavenumber),!is.null(colnames(sp)),setequal(colnames(sp),ids))
# Preserve library IDs as column names and export native axes. Missing coverage
# is handled explicitly in Python; never extrapolate.
common <- file.path(out,"common_reference")
dir.create(common,showWarnings=FALSE)
write.csv(data.frame(wavenumber=raw$wavenumber,sp[,ids,drop=FALSE],check.names=FALSE),file.path(common,"raw_reference.csv"),row.names=FALSE)
write.csv(approved,file.path(common,"reference_metadata.csv"),row.names=FALSE)
message("Common raw references exported: ",length(ids))
