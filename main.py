import pysftp
import re
import logging
import GeodataReader as gr
import ScanCheck

# Defining log
logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.FileHandler("Overseas.log")
logger.addHandler(handler)
formatter=logging.Formatter('%(asctime)s: %(levelname)s - %(message)s')
handler.setFormatter(formatter)

def sftp_download(host, user, passw, remote_dir, local_dir, pattern, sem=True, delete=False):
    with pysftp.Connection(host, username=user, password=passw) as sftp:
        with sftp.cd(remote_dir):  # temporarily chdir to public
            if len(sftp.listdir_attr(remote_dir)) != 0:
                for files in sftp.listdir_attr(remote_dir):
                    # list files that match the regexp pattern if sem- is true we look for semafor files
                    if sem:
                        if re.search(pattern+".sem",files.filename):
                            try:
                                sftp.get(files.filename[:-4], files.filename[:-4])
                                logger.info(files.filename[:-4] + " file downloaded")
                                sftp.remove(files.filename)
                                if delete:
                                    sftp.remove(files.filename[:-4])
                                    logger.info(files.filename[:-4] + " file removed")
                            except Exception as error:
                                logger.critical(
                                    files.filename[:-4] + " error happened while downloading " + str(error))
                    else:
                        if re.search(pattern,files.filename):
                            try:
                                sftp.get(files.filename, files.filename)
                                logger.info(files.filename + "file downloaded")
                            except Exception as error:
                                logger.critical(
                                    files.filename + " error happened while downloading " + str(error))


#sftp_download('62.168.45.122','DPD_HU','I64Wg0j6','/PREPROD/_Customer/Zengtextil','.','GEODATA_SHPNOT_DRK_(\d{7})_D(\d{8})T(\d{6})_(\d{6})',True)

parcel=gr.get_values("GEODATA_SHPNOT_DRK_0171641_D20220704T111925_427095","PARCEL.PARCELNUMBER")
#print(parcel)
result=ScanCheck.get_scan(parcel)
print(result.head())