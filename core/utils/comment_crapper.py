def remove_lines_with_word_and_ending(file_path, word_to_remove, ending_to_remove):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        with open(file_path, 'w') as file:
            for line in lines:
                if word_to_remove not in line or not line.strip().endswith(ending_to_remove):
                    file.write(line)

        print(
            f"Lines containing '{word_to_remove}' and ending with '{ending_to_remove}' removed successfully from '{file_path}'.")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


remove_lines_with_word_and_ending(
    '/home/skywalker/GitHub/GateKeeper/templates/panel/components/page/overview.html',
    '<!--begin:', '-->'
)
remove_lines_with_word_and_ending(
    '/home/skywalker/GitHub/GateKeeper/templates/panel/components/page/overview.html',
    '<!--end:', '-->'
)
