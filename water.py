import tarfile, pathlib, math

# folder_path = pathlib.Path(input('Main Location: '))
# a = filepath.iterdir()
# len(list(filepath.glob('*')))

#   分上下卷的文件用captital


def Rename_hicc_nhen(f_path, capital=''):

    pic_n = len(list(f_path.glob('*.jpg')))
    digits = len(str(pic_n))

    #   default fileorder: 1, 10, 100

    for q in f_path.iterdir():
        if pathlib.PurePath(q).match('*.jpg') and int(q.stem) < math.pow(
                10, digits):
            q.rename(q.parents[0] /
                     (capital + q.stem.rjust(digits, '0') + '.jpg'))
        else:
            q.rename(q.parents[0] / (capital + q.stem + '.jpg'))
