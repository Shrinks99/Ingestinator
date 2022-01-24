
import sys
import nuke

# Init the script by running nuke.scriptOpen(slatemachine.nk) by looking at the launch flags
inScript = sys.argv[4]
nuke.scriptOpen(inScript)
print("---")
print(sys.argv)

# Set values from ingest.py passed along by -t on launch
nukeinputclean = str(sys.argv[1])
lastframe = int(sys.argv[2])
currentcolorfileclean = str(sys.argv[3])
nuke.toNode("renderInput").knob("file").setValue(nukeinputclean)
nuke.toNode("renderInput").knob("last").setValue(lastframe)
nuke.toNode("OCIOCDLTransform1").knob("file").setValue(currentcolorfileclean)

# Execute the global frame length setup button in SlateMachine
nuke.toNode("SlateMachine1").knob("setprojframes").execute()

print(currentcolorfileclean)

# Save the script
nuke.scriptSaveAs(nuke.script_directory() + "/slatemachine.nk", 1)

# Render the script and quit on render complete
nuke.render(nuke.toNode("slatemachineOutputPlate"))

# Disable the plate write node and enable the regular one, reset some SlateMachine1 values
nuke.toNode("slatemachineOutputPlate")['disable'].setValue(0)
nuke.toNode("slatemachineOutput")['disable'].setValue(1)
nuke.toNode("SlateMachine1").knob("task").setValue("")
nuke.toNode("SlateMachine1").knob("completion").setValue("100%")

# Save the script again!
nuke.scriptSaveAs(nuke.script_directory() + "/slatemachine.nk", 1)
quit()