import argparse
import os
import cv2
import librosa
import numpy as np
import soundfile as sf
import torch
from flask_restful import Resource
from tqdm import tqdm
from .lib.nets import CascadedASPPNet
from .lib.dataset import make_padding
from .lib.spec_utils import calc_spec, spec_to_wav, mask_uninformative


class BackgroundEffect(Resource):
    @staticmethod
    def split_vocal(filename, index):
        p = argparse.ArgumentParser()
        p.add_argument('--gpu', '-g', type=int, default=-1)
        p.add_argument('--model', '-m', type=str, default='./models/baseline.pth')
        # p.add_argument('--input', '-i', required=True)
        p.add_argument('--sr', '-r', type=int, default=44100)
        p.add_argument('--hop_length', '-l', type=int, default=1024)
        p.add_argument('--window_size', '-w', type=int, default=512)
        p.add_argument('--out_mask', '-M', action='store_true')
        p.add_argument('--postprocess', '-p', action='store_true')
        args = p.parse_args()

        print('loading model...', end=' ')
        device = torch.device('cpu')
        model = CascadedASPPNet()
        model.load_state_dict(torch.load('Packages/BackgroundEffect/models/baseline.pth', map_location=device))
        if torch.cuda.is_available() and args.gpu >= 0:
            device = torch.device('cuda:{}'.format(args.gpu))
            model.to(device)
        print('done')
        file_path = 'chunk/' + filename + '_chunk' + str(index) + '.wav'
        print('loading wave source...', end=' ')
        new_sr = args.sr
        print(new_sr)
        X, sr = librosa.load(
            file_path, new_sr, False, dtype=np.float32, res_type='kaiser_fast')
        print('done')

        print('stft of wave source...', end=' ')
        X = calc_spec(X, args.hop_length)
        X, phase = np.abs(X), np.exp(1.j * np.angle(X))
        coeff = X.max()
        X /= coeff
        print('done')

        offset = model.offset
        l, r, roi_size = make_padding(X.shape[2], args.window_size, offset)
        X_pad = np.pad(X, ((0, 0), (0, 0), (l, r)), mode='constant')
        X_roll = np.roll(X_pad, roi_size // 2, axis=2)

        model.eval()
        with torch.no_grad():
            masks = []
            masks_roll = []
            for i in tqdm(range(int(np.ceil(X.shape[2] / roi_size)))):
                start = i * roi_size
                X_window = torch.from_numpy(np.asarray([
                    X_pad[:, :, start:start + args.window_size],
                    X_roll[:, :, start:start + args.window_size]
                ])).to(device)
                pred = model.predict(X_window)
                pred = pred.detach().cpu().numpy()
                masks.append(pred[0])
                masks_roll.append(pred[1])

            mask = np.concatenate(masks, axis=2)[:, :, :X.shape[2]]
            mask_roll = np.concatenate(masks_roll, axis=2)[:, :, :X.shape[2]]
            mask = (mask + np.roll(mask_roll, -roi_size // 2, axis=2)) / 2

        if args.postprocess:
            vocal = X * (1 - mask) * coeff
            mask = mask_uninformative(mask, vocal)

        inst = X * mask * coeff
        vocal = X * (1 - mask) * coeff

        basename = os.path.splitext(os.path.basename(file_path))[0]
        basename = 'predict/' + basename
        print('inverse stft of instruments...', end=' ')
        wav = spec_to_wav(inst, phase, args.hop_length)
        print('done')
        sf.write('{}_Instruments.wav'.format(basename), wav.T, int(sr))

        print('inverse stft of vocals...', end=' ')
        wav = spec_to_wav(vocal, phase, args.hop_length)
        print('done')
        sf.write('{}_Vocals.wav'.format(basename), wav.T, int(sr))

        if args.out_mask:
            norm_mask = np.uint8((1 - mask) * 255).transpose(1, 2, 0)
            norm_mask = np.concatenate([
                np.max(norm_mask, axis=2, keepdims=True),
                norm_mask
            ], axis=2)[::-1]
            _, bin_mask = cv2.imencode('.png', norm_mask)
            with open('{}_Mask.png'.format(basename), mode='wb') as f:
                bin_mask.tofile(f)

        return {'status': 'working..!',
                'data': filename,
                'response_code': 1000,
                'Application': 'Research 2020-159-speech_recognition_system',
                'version': '1.0.0'}
