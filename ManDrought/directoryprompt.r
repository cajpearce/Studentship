promptstr = "Enter your absolute directory: "
#directory = readline(prompt=promptstr)
directory = file.choose()

if(!file.exists(directory)) {
	stop("That location does not exist on this computer.")
} elif (!file.info(directory)$isdir) {
	stop("You have provided an invalid directory or a file. Make sure you have provided an absolute directory.")
}


