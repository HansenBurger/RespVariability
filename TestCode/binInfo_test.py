import sys, pathlib

sys.path.append(str(pathlib.Path.cwd().parents[0]))
from Code.Fundal import BinImport, ReadSamplerate

main_loc = r'C:\Main\Data\_\Sample\mode'
folder_list = ['840', 'maquet', 'drager', 'mindray', 'V60', 'G5']

zif_path = pathlib.Path(main_loc) / folder_list[5] / 'ZG88310520081000RC6.zif'
zdt_path = None
zpx_path = pathlib.Path(
    main_loc) / folder_list[5] / 'ZG88310520081000RC6_001.zpx'

zif_output = BinImport.ImportZif(zif_path)
#zdt_output = BinImport.ImportWaveHeader(zdt_path)
zpx_output = BinImport.ImportPara(zpx_path)

machine_name = zif_output['machineType'].split('-')[0]
vent_type = int(zpx_output[0]['st_VENT_TYPE'][0].item())
vent_mode = int(zpx_output[0]['st_VENT_MODE'][0].item())
mand_type = int(zpx_output[0]['st_VENT_TYPE'][0].item())

machine_type = ReadSamplerate.ReadVentMode(machine_name, vent_type, vent_mode,
                                           mand_type)
print(machine_type)
