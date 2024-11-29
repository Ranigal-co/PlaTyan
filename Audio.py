import eyed3
from eyed3.plugins import *
from eyed3.core import *

from PySide6.QtWidgets import *
from PySide6.QtMultimedia import *
from PySide6.QtGui import *
from PySide6.QtCore import *

from database import Database

from struct_player import Struct_Player


class Audio(Struct_Player):
    def __init__(self):
        super().__init__()
        self.DATA = Database('database.db')
        self.constants()
        self.INIT_MAIN()
        self.config_media_signals()
        self.init_override()
        self.load_data()

    def load_data(self):
        lt_playlists = self.DATA.get_playlists()
        lt_songs = self.DATA.get_songs_from_playlist("Все")
        for path_song in lt_songs:
            self.file_logic_load(path_song)
        for playlist in lt_playlists:
            if playlist != "Все":
                self.duration_dict[playlist] = 0
                other_songs = self.DATA.get_songs_from_playlist(playlist)
                for song in other_songs:
                    self.file_logic_load_other(song, playlist)
                self.combo_box.addItem(playlist)

    def file_logic_load_other(self, filename, play_list):
        if filename:
            player2 = QMediaPlayer()
            player2.setSource(QUrl.fromLocalFile(filename))
            player2.play()
            QTimer.singleShot(150, lambda p=player2, song=filename: self.append_file_load_other(p, play_list))

    def append_file_load_other(self, p, play_list):
        self.duration_dict[play_list] += p.duration()

    def file_logic_load(self, filename):
        if filename:
            player2 = QMediaPlayer()
            player2.setSource(QUrl.fromLocalFile(filename))
            player2.play()
            QTimer.singleShot(150, lambda p=player2, song=filename: self.append_file_load(p, song))

    def append_file_load(self, p, song):
        self.media_player.setSource(QUrl.fromLocalFile(song))
        self.media_player.durationChanged.connect(self._update_duration)
        self.count += 1
        self.button_play.setEnabled(True)
        if self.count != 1:
            self.buttons['next'].setEnabled(True)
            self.buttons['back'].setEnabled(True)
        self.status_bar.showMessage(song.split('/')[-1])
        self.options.append(song)
        self.label_song_now.setText('Номер песни: ' + str(self.options.index(song) + 1))

        self.picture_song(song)
        self.info(song)

        self.movie_gif_pic.start()
        self.change_image_pic(self.movie_gif_pic.currentFrameNumber())

        self.movie_gif.start()
        self.change_image(self.movie_gif.currentFrameNumber())

        self.duration_dict["Все"] += p.duration()

        self.label_count.setText('Песен: ' + str(self.count))

        self.list_widget.addItem(f'{0 + len(self.options)} - {song.split('/')[-1]}')
        self.label_duration.setText(self.set_duration_text_on_label_duration(self.duration_dict["Все"]))

    def close(self):
        self.DATA.close()

    def create_playlist(self):
        name, ok = QInputDialog.getText(self, 'Создать плейлист', 'Введите название плейлиста:')
        if ok and name:
            if self.DATA.add_playlist(name):
                self.combo_box.addItem(name)
                self.duration_dict[name] = 0
            else:
                QMessageBox.warning(self, 'Ошибка', 'Плейлист не создан')

    def delete_playlist(self):
        name, ok = QInputDialog.getText(self, 'Удалить плейлист', 'Введите название плейлиста:')
        if ok and name in self.DATA.get_playlists():
            if name != 'Все':
                self.DATA.delete_playlist(name)
                self.combo_box.removeItem(self.combo_box.currentIndex())
                self.duration_dict["Все"] = 0
                self.delete_files()
            else:
                self.DATA.delete_playlist(name)
                self.duration_dict["Все"] = 0
                self.duration_dict[self.combo_box.currentText()] = 0
                self.delete_files()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Плейлист не удален')

    def delete_files(self):
        self.label_duration.setText('00:00:00')
        self.count = 0
        self.labels['timestamp'].setText('00:00 / 00:00')
        self.media_duration_slider.setRange(0, 0)
        self.list_widget.clear()
        self.options.clear()
        self.label_count.setText('Песен: ' + str(self.count))
        self.update_buttons_state()
        self.delete_file()

    def delete_song(self):
        if self.row < 0 or self.row >= len(self.options):
            return
        song_path = self.options[self.row]
        self.duration_song_logic(song_path)

    def duration_song_logic(self, song):
        if song:
            player2 = QMediaPlayer()
            player2.setSource(QUrl.fromLocalFile(song))
            player2.play()
            QTimer.singleShot(150, lambda p=player2, s = song: self.duration_song(p, s))

    def duration_song(self, p, song_path):
        playlist_name = self.combo_box.currentText()
        if self.combo_box.currentText() != "Все":
            if self.duration_dict["Все"] != 0:
                self.duration_dict["Все"] -= p.duration()
            if self.duration_dict[self.combo_box.currentText()] != 0:
                self.duration_dict[self.combo_box.currentText()] -= p.duration()
        else:
            if self.duration_dict["Все"] != 0:
                self.duration_dict["Все"] -= p.duration()
        self.label_duration.setText(
            self.set_duration_text_on_label_duration(
                self.duration_dict[self.combo_box.currentText()]))
        self.DATA.delete_song_from_playlist(song_path, playlist_name)
        self.labels['timestamp'].setText('00:00 / 00:00')
        self.media_duration_slider.setRange(0, 0)
        self.options.remove(song_path)
        self.list_widget.takeItem(self.row)
        self.count -= 1
        self.label_count.setText('Песен: ' + str(self.count))
        if self.row >= len(self.options):
            self.row = len(self.options) - 1
        if self.row >= 0:
            self.list_widget.setCurrentRow(self.row)
        self.update_buttons_state()
        self.delete_file()
        self.list_widget.clear()
        self.list_widget.addItems([f"{i + 1} - {self.options[i].split('/')[-1]}" for i in range(len(self.options))])

    def constants(self):
        self.row = 0
        self.flag_1 = False
        self.flag_2 = 2
        self.count = 0
        self.duration_dict = {}
        self.duration_dict["Все"] = 0

    def init_override(self):
        self.list_widget.currentRowChanged.connect(self.on_itemClicked)

        self.but_cycle_one.clicked.connect(self.clic_cycle_one)
        self.but_cycle_list.clicked.connect(self.clic_cycle_list)
        self.but_cycle_inf.clicked.connect(self.clic_cycle_inf)

        self.change_image_pic(self.movie_gif_pic.currentFrameNumber())

        self.volume_slider.valueChanged.connect(self.set_volume)

        self.buttons['open'].clicked.connect(self.open_file)
        self.button_play.clicked.connect(self.play)
        self.buttons['next'].clicked.connect(self.next)
        self.buttons['back'].clicked.connect(self.back)
        self.media_duration_slider.sliderMoved.connect(self.set_slider_position)

        self.combo_box.currentTextChanged.connect(self.on_itemClicked_box_playlist)

        self.buttons['create_playlist'].clicked.connect(self.create_playlist)
        self.buttons['delete_playlist'].clicked.connect(self.delete_playlist)
        self.buttons['delete_song'].clicked.connect(self.delete_song)

    def set_volume(self, val):
        l = QAudio.convertVolume(val / 100.0, QAudio.VolumeScale.LogarithmicVolumeScale, QAudio.VolumeScale.LinearVolumeScale)
        self.audio_output.setVolume(l)
        self.volume_label.setText(str(val) + '%')

    def clic_cycle_one(self):
        self.flag_2 = 0

    def clic_cycle_list(self):
        self.flag_2 = 1

    def clic_cycle_inf(self):
        self.flag_2 = 2

    def on_itemClicked(self, row):
        if row < 0 or row >= len(self.options):
            return
        self.row = row
        self.change_song_config()
        if self.media_player.playbackState() != QMediaPlayer.PlaybackState.PlayingState:
            self.play_config()
        self.label_song_now.setText('Номер песни: ' + str(self.row + 1))

    def update_buttons_state(self):
        self.button_play.setEnabled(self.count > 0)
        self.buttons['next'].setEnabled(self.count > 1)
        self.buttons['back'].setEnabled(self.count > 1)

    def file_logic(self, filename):
        if filename:
            player2 = QMediaPlayer()
            player2.setSource(QUrl.fromLocalFile(filename))
            player2.play()
            QTimer.singleShot(150, lambda p=player2, song=filename: self.append_file(p, song))

    def open_file(self):
        songs, _ = QFileDialog.getOpenFileNames(self, 'Select Folder', '.', 'Audio files (*.mp3 *.wav)')
        if songs:
            for song in songs:
                self.file_logic(song)

    def info(self, filename):
        aud_file = eyed3.load(filename)
        if aud_file is None:
            self.label_song.setText('Песня: пусто')
            self.label_autor.setText('Автор: пусто')
            self.label_album.setText('Альбом: пусто')
            self.label_genre.setText('Жанр: пусто')
            self.label_year.setText('Год: пусто')
            return
        if aud_file.tag.title:
            self.label_song.setText('Песня: ' + str(aud_file.tag.title))
        else:
            self.label_song.setText('Песня: пусто')
        if aud_file.tag.artist:
            self.label_autor.setText('Автор: ' + str(aud_file.tag.artist))
        else:
            self.label_autor.setText('Автор: пусто')
        if aud_file.tag.album:
            self.label_album.setText('Альбом: ' + str(aud_file.tag.album))
        else:
            self.label_album.setText('Альбом: пусто')
        if aud_file.tag.genre:
            self.label_genre.setText('Жанр: ' + str(aud_file.tag.genre))
        else:
            self.label_genre.setText('Жанр: пусто')
        if aud_file.tag.recording_date:
            self.label_year.setText('Год: ' + str(aud_file.tag.recording_date))
        else:
            self.label_year.setText('Год: пусто')

    def picture_song(self, filename):
        try:
            self.label_secret_pic.setText('')
            aud_file = eyed3.load(filename)
            if aud_file is None:
                self.flag_1 = False
                self.label_secret_pic.setText('Изображение не найдено')
                return
            self.flag_1 = True
            images = aud_file.tag.images
            if images is None and images == False:
                self.label_secret_pic.setText('Изображение не найдено')
                self.flag_1 = False
                return
            with open('song.jpg', 'wb+') as file:
                file.write(images[0].image_data)
            img_pixmap = QPixmap('song.jpg')
            img_pixmap = img_pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)
            self.label_pic.setPixmap(img_pixmap)
        except Exception as e:
            self.label_secret_pic.setText('Изображение не найдено')
            self.flag_1 = False
            print(e)
            return

    def delete_file(self):
        self.media_player.stop()
        self.label_song.setText('Песня: ')
        self.label_autor.setText('Автор: ')
        self.label_album.setText('Альбом: ')
        self.label_genre.setText('Жанр: ')
        self.label_year.setText('Год: ')
        self.labels['timestamp'].setText('00:00 / 00:00')
        self.label_song_now.setText('0')
        self.status_bar.showMessage('')
        self.flag_1 = False

        if self.flag_1 == False:
            self.change_image_pic(self.movie_gif_pic.currentFrameNumber())
            self.change_image(self.movie_gif.currentFrameNumber())

    def append_file(self, p, song):
        self.media_player.setSource(QUrl.fromLocalFile(song))
        self.media_player.durationChanged.connect(self._update_duration)
        self.count += 1
        self.button_play.setEnabled(True)
        if self.count != 1:
            self.buttons['next'].setEnabled(True)
            self.buttons['back'].setEnabled(True)
        self.status_bar.showMessage(song.split('/')[-1])
        self.options.append(song)
        self.label_song_now.setText('Номер песни: ' + str(self.options.index(song) + 1))

        self.picture_song(song)
        self.info(song)

        self.movie_gif_pic.start()
        self.change_image_pic(self.movie_gif_pic.currentFrameNumber())

        self.movie_gif.start()
        self.change_image(self.movie_gif.currentFrameNumber())
        if self.combo_box.currentText() != "Все":
            self.duration_dict["Все"] += p.duration()
            self.duration_dict[self.combo_box.currentText()] += p.duration()
        else:
            self.duration_dict["Все"] += p.duration()

        self.list_widget.addItem(f'{0 + len(self.options)} - {song.split('/')[-1]}')
        self.label_duration.setText(self.set_duration_text_on_label_duration(self.duration_dict[self.combo_box.currentText()]))

        if self.DATA.add_song_to_playlist(song, self.combo_box.currentText()):
            self.label_count.setText('Песен: ' + str(self.count))
            self.update_buttons_state()
        else:
            QMessageBox.warning(self, 'Error', 'Failed to add song to playlist')

    def _update_duration(self, duration):
        duration_second = duration / 1000
        minutes = int(duration_second / 60)
        seconds = int(duration_second % 60)
        self.labels['timestamp'].setText(f'00:00 / {minutes:02d}:{seconds:02d}')

    def config_media_signals(self):
        self.media_player.playbackStateChanged.connect(self.on_media_state_changed)
        self.media_player.positionChanged.connect(self.on_position_changed)
        self.media_player.durationChanged.connect(self.on_duration_changed)
        self.media_player.errorChanged.connect(self.error_handler)

    def on_position_changed(self, position):
        self.media_duration_slider.setValue(position)
        self.labels['timestamp'].setText(self.format_position(position))
        if self.media_duration_slider.value() == self.media_duration_slider.maximum():
            self.change_image(self.movie_gif.currentFrameNumber())
            self.change_image_pic(self.movie_gif_pic.currentFrameNumber())

            if self.flag_2 == 0:
                self.change_song_config()
                self.play_config()
            elif self.flag_2 == 1:
                if (self.row + 1) < len(self.options):
                    self.row += 1
                    self.list_widget.setCurrentRow(self.row)
                    self.change_song_config()
                    self.play_config()
            else:
                self.row = (self.row + 1) % len(self.options)
                self.list_widget.setCurrentRow((self.row) % len(self.options))
                self.change_song_config()
                self.play_config()

    def format_position(self, position):
        seconds = (position / 1000) % 60
        minutes = (position / (1000 * 60)) % 60

        duration = self.media_player.duration()
        total_seconds = (duration / 1000) % 60
        total_minutes = (duration / (1000 * 60)) % 60

        return "%02d:%02d / %02d:%02d" % (minutes, seconds, total_minutes, total_seconds)

    def on_duration_changed(self, duration):
        self.media_duration_slider.setRange(0, duration)

    def on_media_state_changed(self):
        if self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.button_play.setIcon(QPixmap('icon/pause.png'))
        else:
            self.button_play.setIcon(QPixmap('icon/play.png'))

    def error_handler(self):
        self.button_play.setEnabled(False)
        self.status_bar.showMessage('Error:' + self.media_player.errorString())

    def set_slider_position(self, position):
        self.media_player.setPosition(position)

    def play(self):
        if self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.media_player.pause()

            self.change_image(self.movie_gif.currentFrameNumber())
            if self.flag_1 == False:
                self.change_image_pic(self.movie_gif_pic.currentFrameNumber())
        else:
            self.play_config()

    def next(self):
        self.row = (self.row + 1) % len(self.options)
        self.change_song_config()
        self.play_config()

    def back(self):
        self.row = (self.row - 1) % len(self.options)
        self.change_song_config()
        self.play_config()

    def change_image(self, index):
        self.pixmap_gif = QPixmap(f"image/im_1/{index + 1}.jpeg")
        self.label_gif.setPixmap(self.pixmap_gif)

    def change_image_pic(self, index):
        if self.flag_1:
            return
        pixmap = QPixmap(f"image/im_2/{index + 1}.jpeg")
        self.label_pic.setPixmap(pixmap)

    def play_config(self):
        self.media_player.play()

        self.label_gif.setMovie(self.movie_gif)
        # self.movie_gif.setSpeed(114)
        self.movie_gif.start()
        if self.flag_1 == False:
            self.label_pic.setMovie(self.movie_gif_pic)
            # self.movie_gif_pic.setSpeed(100)
            self.movie_gif_pic.start()

    def change_song_config(self):
        self.song = self.options[self.row]
        self.media_player.setSource(QUrl.fromLocalFile(self.song))

        self.media_player.durationChanged.connect(self._update_duration)
        self.button_play.setEnabled(True)
        self.status_bar.showMessage(self.song.split('/')[-1])
        self.label_song_now.setText('Номер песни: ' + str(self.options.index(self.song) + 1))

        self.picture_song(self.song)
        self.info(self.song)

        self.movie_gif_pic.start()
        self.change_image_pic(self.movie_gif_pic.currentFrameNumber())

        self.movie_gif.start()
        self.change_image(self.movie_gif.currentFrameNumber())

    def on_itemClicked_box_playlist(self, item):
        self.options = self.DATA.get_songs_from_playlist(item)
        self.list_widget.clear()
        self.label_duration.setText(self.set_duration_text_on_label_duration(self.duration_dict[self.combo_box.currentText()]))
        self.list_widget.addItems([f"{i + 1} - {self.options[i].split('/')[-1]}" for i in range(len(self.options))])
        self.count = len(self.options)
        self.label_count.setText('Песен: ' + str(self.count))
        self.update_buttons_state()

    def set_duration_text_on_label_duration(self, duration):
        h1 = duration // 1000 // 60 // 60 % 60
        m1 = duration // 1000 // 60 % 60
        s1 = duration // 1000 % 60
        return f'{h1:0>2}:{m1:0>2}:{s1:0>2}'


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    os.environ['QT_MULTIMEDIA_PREFERRED_PLUGINS'] = 'windowsmediafoundation'
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app_window = Audio()
    app_window.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
    app_window.close()