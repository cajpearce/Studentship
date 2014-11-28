# EDIT THIS IN FUTURE
inputtype = "CSV"

promptstr = paste("Enter your absolute", inputtype, "directory: ")
directory = readline(prompt=promptstr)

if(!file.exists(directory)) {
	stop("That location does not exist on this computer.")
} elif (!file.info(directory)$isdir) {
	stop("You have provided an invalid directory or a file. Make sure you have provided an absolute directory.")
}


