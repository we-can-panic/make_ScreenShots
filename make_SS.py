"""
・手順書を簡単にするプログラム

1. Alt+PrintScreenで撮りたいウィンドウを「スクリーンショット」下に「master.png」保存
2. Win+PrintScreenで全体を撮る（撮りたいウィンドウは1.で撮った状態と1px単位で同じであること！）
3. あとはソフトを操作しながらWin+PrintScreenで自動保存していく
4. このプログラムを動かす
"""

import os, re, time
import cv2
import tqdm
import numpy as np


def main():
  print("Start")
  SS_PATH = "C:\\Users\\koshi\\OneDrive\\画像\\スクリーンショット\\"
  if SS_PATH=="":
    SS_PATH = input("Enter ScreenShots's Path: ")
  SS_output_PATH = SS_PATH + "outputs\\"
  if not os.path.isdir(SS_output_PATH):
    os.mkdir(SS_output_PATH)

  SS_re = re.compile("スクリーンショット \\([0-9]*\\).png")
  SS_num_re = re.compile("[0-9]+")

  img_path_list = list(filter(lambda x: SS_re.match(x), os.listdir(SS_PATH)))
  img_path_list.sort(key=lambda x: int(SS_num_re.search(x).group()))

  mstr = imread(SS_PATH+"master.png")
  dcpl = imread(SS_PATH+img_path_list[0])

  top, bottom, left, right = find_place(mstr, dcpl)

  for img_name in img_path_list:
    img_in = SS_PATH+img_name
    img_out = SS_output_PATH+img_name
    trim_img = imread(img_in)
    imwrite(img_out, trim_img[top: bottom, left: right])

  print(len(img_path_list), "images has clipped at", SS_output_PATH)

def find_place(mstr, dcpl):
  h, w = mstr.shape[:2]
  first_pixel = mstr[0][0].sum()
  i_cdd, j_cdd = np.where(dcpl.sum(axis=2)==first_pixel)
  for i,j in zip(i_cdd, j_cdd):
    if np.all(mstr==dcpl[i: i+h, j: j+w]):
      print("find!")
      return i, i+h, j, j+w


def imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
  try:
    n = np.fromfile(filename, dtype)
    img = cv2.imdecode(n, flags)
    return img
  except Exception as e:
    print(e)
    return None


def imwrite(filename, img, params=None):
  try:
    ext = os.path.splitext(filename)[1]
    result, n = cv2.imencode(ext, img, params)
    if result:
      with open(filename, mode='w+b') as f:
        n.tofile(f)
      return True
    else:
      return False
  except Exception as e:
    print(e)
    return False


if __name__ == '__main__':
  main()
