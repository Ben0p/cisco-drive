

'''

def get():
    required_settings = ['template', 'hostname', 'ip', 'prefix', 'suffix', 'case', 'temp', 'test', 'com']
    line_count = 0
    while True:
        if os.path.isdir("settings"):
            if os.path.exists("settings/settings.txt"):
                with open('settings/settings.txt') as f:
                    for line in f:
                        line_count =+ 1
                        line = line.strip()
                        line = line.split('=')
                        setting = line[0]
                        param = line[1]
                        settings[setting] = param
                if line_count == 0:
                    print("Config is blank, populating parameters...")
                    missing_setting = False
                    generate()
                elif line_count > 0:
                    settings_in_file = []
                    for key, value in settings.items():
                        settings_in_file.append(key)
                    if len(settings_in_file) < len(required_settings):
                        missing_setting = True
                    else:
                        missing_setting = False
                    
                if missing_setting:
                    print("Required settings missing in settings file, starting wizard")
                    generate()
                    missing_setting = False
                return(settings)
            else:
                print("settings/settings.txt not found, creating file...")
                generate()
        else:
            print("No settings directory found, creating directory...")
            generate()

'''