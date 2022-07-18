from PIL import Image

def scale_gif(path, new_path=None):
    gif = Image.open(path)
    if not new_path:
        new_path = path
    if path[-3:] == "gif":
        old_gif_information = {
            'loop': bool(gif.info.get('loop', 1)),
            'duration': gif.info.get('duration', 40),
            'background': gif.info.get('background', 223),
            'extension': gif.info.get('extension', (b'NETSCAPE2.0')),
            'transparency': gif.info.get('transparency', 223)
        }
        if gif.width >= 1080:
            new_width = 1060
            new_height = round(gif.height / (gif.width / new_width))
            if gif.height > 1194:
                new_height = 1194
                new_width = round(gif.width / (gif.height / new_height))
            print((new_width, new_height))
            new_frames = get_new_frames(gif, (new_width, new_width))
        else:
            print((gif.width, gif.height))
            new_frames = get_new_frames(gif, (gif.width, gif.height))
        save_new_gif(new_frames, old_gif_information, new_path)
    else:
        if gif.width >= 1080:
            new_width = 1060
            new_height = round(gif.height / (gif.width / new_width))
            gif = gif.resize((new_width, new_height))
            if gif.height > 1194:
                new_height = 1194
                new_width = round(gif.width / (gif.height / new_height))
                gif = gif.resize((new_width, new_height))
        gif.save(path)


def get_new_frames(gif, scale):
    new_frames = []
    actual_frames = gif.n_frames
    for frame in range(actual_frames):
        gif.seek(frame)
        new_frame = Image.new('RGBA', gif.size)
        new_frame.paste(gif)
        new_frame = new_frame.resize(scale, Image.ANTIALIAS)
        new_frames.append(new_frame)
    return new_frames

def save_new_gif(new_frames, old_gif_information, new_path):
    new_frames[0].save(new_path,
                       save_all = True,
                       append_images = new_frames[1:],
                       duration = old_gif_information['duration'],
                       loop = old_gif_information['loop'],
                       background = old_gif_information['background'],
                       extension = old_gif_information['extension'] ,
                       transparency = old_gif_information['transparency'])


if __name__ == "__main__":
    scale_gif(f"Post-qtehpj.gif", (1080,1920),"test.gif")