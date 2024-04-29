from llama_index.tools import FunctionTool
import os

note_file = os.path.join("data","notes.txt")

def save_notes(note):
    if not os.path.exists(note_file):
        open(note_file, 'w')

    with open(note_file, 'w') as f:
        f.writelines([note + "\n"])

    return "note saved to " + note_file

note_engine = FunctionTool.from_defaults(
    fn = save_notes,
    name = "note_saver",
    description = " this tool is used to save notes for the user",
)


