import os
import tempfile

from datetime import datetime
from django.db import models
from django.urls import reverse
from smb.smb_structs import OperationFailure
from .instance import Instance
from .smb_directory import SMBDirectory


class SMBFileManager(models.Manager):
    def update_smb(self, instance: SMBDirectory):
        files = instance.list_all_files()
        for f in files:
            found = instance.file_set.filter(path=f).first()
            if not found:
                new_file = SMBFile(
                    path=f,
                    source=instance,
                )
                new_file.save()
        instance.last_sync = datetime.now()
        instance.save()


class SMBFile(models.Model):
    path = models.CharField(max_length=500, blank=False)
    is_archived = models.BooleanField(default=False)
    source = models.ForeignKey(
        SMBDirectory,
        related_name='file_set',
        on_delete=models.PROTECT,
    )

    objects = SMBFileManager()

    class Meta:
        verbose_name_plural = "SMB Files"

    def get_absolute_url(self):
        return reverse('smb_file_list')

    def get_file(self):
        connection = self.source.connect()
        temp_file = tempfile.NamedTemporaryFile()
        connection.retrieveFile(
            self.source.share_name,
            self.path,
            temp_file,
        )
        connection.close()
        temp_file.seek(0)
        return temp_file

    def archive(self):
        temp_file = self.get_file()
        instance = Instance.objects.from_dcm(temp_file)
        self.is_archived = True
        self.save()
        return instance

    @property
    def dir_name(self):
        return os.path.dirname(self.path)

    @property
    def is_available(self):
        connection = self.source.connect()
        try:
            dir_files = connection.listPath(
                self.source.share_name,
                self.dir_name,
            )
            connection.close()
        except OperationFailure:
            return False
        file_names = [f.filename for f in dir_files]
        if os.path.basename(self.path) in file_names:
            return True
        return False