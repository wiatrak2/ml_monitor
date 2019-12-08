import jinja2
import getpass

gdrive_settings_tpl_path = "ml_monitor/gdrive/settings.yaml.j2"

with open(gdrive_settings_tpl_path) as f:
    gdrive_settings_tpl_string = f.read()

gdrive_settings_tpl = jinja2.Template(gdrive_settings_tpl_string)

client_id = getpass.getpass("client_id:")
client_secret = getpass.getpass("client_secret:")

gdrive_settings_file = gdrive_settings_tpl_path[:-3]
gdrive_settings = gdrive_settings_tpl.render(client_id=client_id, client_secret=client_secret)
with open(gdrive_settings_file, "w") as f:
    f.write(gdrive_settings)
