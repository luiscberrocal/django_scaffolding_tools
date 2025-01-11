from pathlib import Path

from jinja2 import Environment, FileSystemLoader

# Set up the Jinja2 environmentte

template_path = Path(__file__).parent
file_loader = FileSystemLoader(template_path)
env = Environment(loader=file_loader)

# Load the template
template = env.get_template('list.html.j2')

# Define the context
context = {
    'header1_content': 'Transactions List'
}

# Render the template with the context
output = template.render(context)

# Print or save the rendered output
print(output)
