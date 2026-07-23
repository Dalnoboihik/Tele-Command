import json
import os
from datetime import datetime

class SystemLogger:
    def __init__(self, log_file='system_stats.log', stats_file='stats.json'):
        self.log_file = log_file
        self.stats_file = stats_file
        self.stats = self._load_stats()
    
    def _load_stats(self):
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {'history': [], 'max_cpu': 0, 'max_ram': 0}
        return {'history': [], 'max_cpu': 0, 'max_ram': 0}
    
    def _save_stats(self):
        with open(self.stats_file, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, ensure_ascii=False, indent=2)
    
    def add_record(self, cpu_percent, ram_percent):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"{timestamp} - CPU: {cpu_percent}%, RAM: {ram_percent}%\n")
        
        record = {'time': timestamp, 'cpu': cpu_percent, 'ram': ram_percent}
        self.stats['history'].append(record)
        
        if len(self.stats['history']) > 1000:
            self.stats['history'] = self.stats['history'][-1000:]
        
        self.stats['max_cpu'] = max(self.stats['max_cpu'], cpu_percent)
        self.stats['max_ram'] = max(self.stats['max_ram'], ram_percent)
        
        self._save_stats()
    
    def get_recent_stats(self, count=100):
        return self.stats['history'][-count:]
    
    def get_max_values(self):
        return {
            'max_cpu': self.stats['max_cpu'],
            'max_ram': self.stats['max_ram']
        }