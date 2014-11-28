# EDIT THIS IN FUTURE
inputtype = "CSV"

promptstr = paste("Enter your absolute", inputtype, "directory: ")
external.file = readline(prompt=promptstr)

if(!file.exists(external.file)) {
	stop("That file does not exist on this computer.")
} elif (file.info(external.file)$isdir) {
	stop("You have provided an invalid file or a directory. Make sure you have provided an absolute file location.")
}


