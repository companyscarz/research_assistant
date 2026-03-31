from speech.tts import speak_out

def create_file_handler(file_path):
    """
    A wrapper function that provides inner functions for 
    reading from and writing to a specific file.
    """
    
    def read_content():
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            speak_out(f"Error: {file_path} does not exist.")
            #return f"Error: {file_path} does not exist."

    def write_content(data, append=False):
        # 'a' mode appends to the end, 'w' overwrites the file
        mode = 'a' if append else 'w'
        try:
            with open(file_path, mode, encoding='utf-8') as f:
                f.write(data)
            #Successfully written"
            speak_out(f"Successfully written to {file_path}.")
        except Exception as e:
            #unsuccessfully written"
            speak_out(f"Failed to write!")
            #return f"Failed to write: {e}"

    # Return both functions so they can be used outside
    return read_content, write_content

    #_______________How to use it___________________________________
    # Define which file we are working with
    #intialize the function first
#get_text, save_text = create_file_handler('my_data.txt')

    #saving the text file
    # This creates/overwrites the file
#save_text("Hello! This is the first line.\n")

    # This adds a second line without deleting the first
#save_text("This is an appended line.", append=True)

    #reading the text file
#current_data = get_text()
#print("File Content:")
#print(current_data)