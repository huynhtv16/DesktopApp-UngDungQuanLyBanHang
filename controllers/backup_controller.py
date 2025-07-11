from models.backup_model import BackupModel

class BackupController:
    def __init__(self):
        self.model = BackupModel()

    def create_backup(self):
        return self.model.create_backup()

    def restore_backup(self, backup_file):
        return self.model.restore_backup(backup_file)