def parse_distribution_file_Debian(self, name, data, path, collected_facts):
    debian_facts = {}
    if 'Debian' in data or 'Raspbian' in data:
        debian_facts['distribution'] = 'Debian'
    elif 'Ubuntu' in data:
        debian_facts['distribution'] = 'Ubuntu'
    elif 'SteamOS' in data:
        debian_facts['distribution'] = 'SteamOS'
    return debian_facts
