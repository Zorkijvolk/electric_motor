import vtkplotlib as vpl

# Set up a figure.
fig = vpl.figure()
# With some stuff in it.
vpl.quick_test_plot()

# Define a function to be run on left mouse click.
def callback(invoker, event_name):
    # These will always be true. Just for demonstration purposes.
    assert invoker is fig.style
    assert event_name == "LeftButtonPressEvent"

    # Respond to the click. fig.iren.GetEventPosition() tells us where (in
    # 2D) the click happened. Converting to 3D is explained later...
    print("You clicked at", fig.iren.GetEventPosition())

    # Call the original behaviour. Otherwise left clicking will cease to do
    # what it used to do. i.e. rotate the camera. Again, explained later...
    vpl.i.call_super_callback()

# Register the (event-type, callback) pair with `fig.style`.
fig.style.AddObserver("LeftButtonPressEvent", callback)

# Then show. `vpl.show()` would also work.
fig.show()