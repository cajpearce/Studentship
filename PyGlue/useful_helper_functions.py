def line_var_transferer(filename, line):
        with open(filename, 'r+') as f:
                content = f.read()
                f.seek(0, 0)
                f.write(line.rstrip('\r\n') + '\n' + content)
        
def copy_file_to_temp_directory(path,append_to_start='',append_to_end=''):
        '''
        with open("infile") as f1:
                with open("outfile", "w") as f2:
                        f2.write("#test firstline")
                        for line in f1:
                                f2.write(line)
        '''
        # modified from TorelTwiddler's code
        # http://stackoverflow.com/questions/6587516/how-to-concisely-create-a-temporary-file-that-is-a-copy-of-another-file-in-pytho
        if not os.path.isfile(path):
                raise Exception("You are trying to use a path instead of a file for your module.")
        temp_dir = tempfile.gettempdir()
        #temp_path = os.path.join(temp_dir, os.path.basename(path))
        temp_path = os.path.join(temp_dir, "test_python_script.py") #could techinically be less generic
        shutil.copy2(path, temp_path)

        # adds the temp directory to the system path to make it easier to import
        # does that mean I'll need to change the 
        sys.path.append(temp_dir)
        
#if len(append_to_start) > 0 or len(append_to_end) < 0:
                #do something fucking cool here m8
                         
        return temp_path
