from PySide6.QtWidgets import *
from PySide6.QtMultimedia import *
from PySide6.QtGui import *
from PySide6.QtCore import *

class Struct_Player(QWidget):
    def __init__(self):
        super().__init__()
        self.init_widget()
        self.set_festive_anime_style()
        self.set_custom_cursor()

    def set_festive_anime_style(self):
        style = """
            QWidget 
            {
                background-color: #222222;
                color: #FFFFFF;
                font-family: "Comic Sans MS";
            }
            QPushButton 
            {
                background-color: #333333;
                border: 1px solid #555555;
                padding: 5px;
                border-radius: 5px;
            }
            QPushButton:hover 
            {
                background-color: #444444;
            }
            QPushButton:pressed 
            {
                background-color: #555555;
            }
            QLabel 
            {
                color: #FF69B4;
            }
            QComboBox 
            {
                background-color: #333333;
                border: 1px solid #555555;
                padding: 5px;
                border-radius: 5px;
                selection-background-color: #444444;
                color: #FFFFFF;
            }
            QComboBox QListView 
            {
                background-color: #333333;
                color: #FFFFFF;
                border: 1px solid #555555;
            }
            QListWidget 
            {
                background-color: #333333;
                border: 1px solid #555555;
                color: #FFFFFF;
                padding: 5px;
                border-radius: 5px;
            }
            QListWidget::item:selected 
            {
                background-color: #444444;
            }
            QSlider::groove:horizontal 
            {
                background: #555555;
                height: 10px;
                border-radius: 5px;
            }
            QSlider::handle:horizontal 
            {
                background: #888888;
                border: none;
                width: 20px;
                margin: -5px 0;
                border-radius: 10px;
            }
            QSlider::groove:vertical 
            {
                background: #555555;
                width: 10px;
                border-radius: 5px;
            }
            QSlider::handle:vertical 
            {
                background: #888888;
                border: none;
                height: 20px;
                margin: 0 -5px;
                border-radius: 10px;
            }
            QStatusBar {
                background-color: #333333;
                border-top: 1px solid #555555;
                color: #FFFFFF;
            }
        """
        self.setStyleSheet(style)

    def set_custom_cursor(self):
        cursor_pixmap = QPixmap('icon/plist.png')
        cursor = QCursor(cursor_pixmap.scaled(50, 50))
        self.setCursor(cursor)

    def INIT_MAIN(self):
        self.init_list()
        self.init_label_playlist()
        self.init_buttons_cycle()
        self.init_ui()

    def init_widget(self):
        self.setWindowTitle('PlaTyan')
        self.setWindowIcon(QPixmap('icon/window.jpg'))
        self.setFixedWidth(940)
        self.setFixedHeight(300)

        self.movie_gif = QMovie("gif/an_1.gif")
        self.movie_gif_pic = QMovie("gif/an_2.gif")
        self.layout = {}
        self.layout['main'] = QVBoxLayout()
        self.setLayout(self.layout['main'])

        self.layout['settings'] = QHBoxLayout()
        self.layout['bar_song'] = QHBoxLayout()
        self.layout['main'].addLayout(self.layout['settings'])
        self.layout['main'].addLayout(self.layout['bar_song'])

        self.layout['picture'] = QVBoxLayout()
        self.layout['info'] = QVBoxLayout()
        self.layout['songList'] = QVBoxLayout()
        self.layout['volume'] = QVBoxLayout()
        self.layout['gif'] = QVBoxLayout()
        self.layout['labels_playlist'] = QHBoxLayout()
        self.layout['btn_pl_song'] = QVBoxLayout()

        self.layout['settings'].addLayout(self.layout['picture'])
        self.layout['settings'].addLayout(self.layout['info'])
        self.layout['settings'].addLayout(self.layout['volume'])
        self.layout['settings'].addLayout(self.layout['songList'])
        self.layout['settings'].addLayout(self.layout['btn_pl_song'])
        self.layout['settings'].addLayout(self.layout['gif'])
        self.layout['songList'].addLayout(self.layout['labels_playlist'])

    def init_ui(self):
        self.buttons = {}
        self.labels = {}

        self.status_bar = QStatusBar()
        self.label_song_now = QLabel()
        self.layout['bar_song'].addWidget(self.status_bar)
        self.layout['bar_song'].addWidget(self.label_song_now)

        self.init_volume_slider()

        self.init_gif()
        self.init_media_player()
        self.init_picture_song()
        self.init_info()

    def init_info(self):
        self.label_song = QLabel('Песня: ')
        self.label_autor = QLabel('Автор: ')
        self.label_album = QLabel('Альбом: ')
        self.label_year = QLabel('Год: ')
        self.label_genre = QLabel('Жанр: ')

        self.layout['info'].addWidget(self.label_song)
        self.layout['info'].addWidget(self.label_autor)
        self.layout['info'].addWidget(self.label_album)
        self.layout['info'].addWidget(self.label_year)
        self.layout['info'].addWidget(self.label_genre)

    def init_picture_song(self):
        self.label_secret_pic = QLabel()
        self.label_pic = QLabel()
        self.layout['picture'].addWidget(self.label_secret_pic)
        self.layout['picture'].addWidget(self.label_pic)
        self.label_pic.setMovie(self.movie_gif_pic)
        self.movie_gif_pic.start()

    def init_volume_slider(self):
        self.volume_slider = QSlider(Qt.Orientation.Vertical)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(75)

        self.volume_label = QLabel('75%')

        self.layout['volume'].addWidget(self.volume_slider)
        self.layout['volume'].addWidget(self.volume_label)

    def init_gif(self):
        self.label_gif = QLabel(self)
        self.label_secret_gif = QLabel()
        self.pixmap_gif = QPixmap("image/im_1/1.jpeg")
        self.label_gif.setPixmap(self.pixmap_gif)
        self.layout['gif'].addWidget(self.label_secret_gif)
        self.layout['gif'].addWidget(self.label_gif)

    def init_media_player(self):
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(0.3)

        self.layout['media_player'] = QHBoxLayout()
        self.layout['main'].addLayout(self.layout['media_player'])

        self.layout['buttons'] = QHBoxLayout()
        self.layout['media_player'].addLayout(self.layout['buttons'])

        self.buttons['open'] = QPushButton()
        self.buttons['create_playlist'] = QPushButton()
        self.buttons['delete_playlist'] = QPushButton()
        self.buttons['delete_song'] = QPushButton()
        self.buttons['open'].setIcon(QPixmap('icon/open.png'))
        self.buttons['create_playlist'].setIcon(QPixmap('icon/create_playlist.png'))
        self.buttons['delete_playlist'].setIcon(QPixmap('icon/delete_playlist.png'))
        self.buttons['delete_song'].setIcon(QPixmap('icon/delete_song.png'))

        self.button_play = QPushButton()
        self.button_play.setEnabled(False)
        self.button_play.setIcon(QPixmap('icon/play.png'))

        self.buttons['next'] = QPushButton()
        self.buttons['next'].setEnabled(False)
        self.buttons['next'].setIcon(QPixmap('icon/next.png'))

        self.buttons['back'] = QPushButton()
        self.buttons['back'].setEnabled(False)
        self.buttons['back'].setIcon(QPixmap('icon/back.png'))

        self.layout['buttons'].addWidget(self.buttons['back'])
        self.layout['buttons'].addWidget(self.button_play)
        self.layout['buttons'].addWidget(self.buttons['next'])

        self.labels['timestamp'] = QLabel('00:00 / 00:00')
        self.layout['media_player'].addWidget(self.labels['timestamp'])

        self.media_duration_slider = QSlider(Qt.Orientation.Horizontal)
        self.media_duration_slider.setFixedWidth(400)
        self.media_duration_slider.setRange(0, 0)
        self.layout['media_player'].addWidget(self.media_duration_slider)
        self.layout['media_player'].addStretch()

        self.layout['media_player'].addWidget(self.buttons['open'])
        self.layout['media_player'].addWidget(self.buttons['delete_song'])
        self.layout['media_player'].addWidget(self.buttons['create_playlist'])
        self.layout['media_player'].addWidget(self.buttons['delete_playlist'])

    def init_list(self):
        self.list_widget = QListWidget()
        self.options = []
        self.list_widget.addItems([s.split('/')[-1] for s in self.options])
        self.layout['songList'].addWidget(self.list_widget)

        self.button_cycle_layout = QHBoxLayout()
        self.layout['songList'].addLayout(self.button_cycle_layout)

    def init_label_playlist(self):
        self.combo_box = QComboBox()
        self.combo_box.addItem('Все')
        self.label_count = QLabel('Песен: 0')
        self.label_duration = QLabel('00:00:00')
        self.layout['labels_playlist'].addWidget(self.combo_box)
        self.layout['labels_playlist'].addWidget(self.label_count)
        self.layout['labels_playlist'].addWidget(self.label_duration)

    def init_buttons_cycle(self):
        self.but_cycle_one = QPushButton()
        self.but_cycle_one.setIcon(QPixmap('icon/cycle_one.png'))
        self.but_cycle_list = QPushButton()
        self.but_cycle_list.setIcon(QPixmap('icon/cycle_list.png'))
        self.but_cycle_inf = QPushButton()
        self.but_cycle_inf.setIcon(QPixmap('icon/cycle_inf.png'))

        self.button_cycle_layout.addWidget(self.but_cycle_one)
        self.button_cycle_layout.addWidget(self.but_cycle_list)
        self.button_cycle_layout.addWidget(self.but_cycle_inf)