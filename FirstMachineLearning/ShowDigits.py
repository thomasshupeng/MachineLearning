from sklearn import datasets
from tkinter import *

GRID_SIZE = 8


class MainWindow:
    nav_index = 0
    index_string = None

    gamma_string = "Auto"
    gamma_entry = None

    bitmap_block = [[None for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]
    expected = None
    predicted = None

    label_img_index = None

    def __init__(self):
        self.root = Tk()
        self.create_main_window()
        self.digits = datasets.load_digits()
        self.expected_string = StringVar()
        self.predicted_string = StringVar()
        return

    def run(self):
        if self.root:
            self.root.mainloop()
        return

    def create_main_window(self):
        top_frame = Frame(self.root)
        top_frame.pack(side=TOP)

        input_frame = Frame(top_frame)
        input_frame.pack(side=TOP)
        label_gamma = Label(input_frame, text="Gamma =")
        label_gamma.pack(side=LEFT)

        self.gamma_string = StringVar()
        self.gamma_entry = Entry(input_frame, textvariable=self.gamma_string)
        self.gamma_string.set("Auto")
        self.gamma_entry.pack(side=LEFT)
        train_btn = Button(input_frame, text="Re-train", command=self.cmd_retrain)
        train_btn.pack(side=LEFT)

        bitmap_frame = Frame(top_frame)
        bitmap_frame.pack(side=BOTTOM)

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                bitmaplable = Label(bitmap_frame, text="     ", bg='#FFFFFF')
                bitmaplable.grid(row=row, column=col, sticky=W, padx=1, pady=1)
                self.bitmap_block[row][col] = bitmaplable

        bottom_frame = Frame(self.root)
        bottom_frame.pack(side=BOTTOM)

        pre_btn = Button(bottom_frame, text="Previous", command=self.go_pre)
        pre_btn.pack(side=LEFT)

        self.label_img_index = Label(bottom_frame, text="Jump to")
        self.label_img_index.pack(side=LEFT)

        self.index_string = StringVar()
        entry_img_index = Entry(bottom_frame, text="0", textvariable=self.index_string)
        entry_img_index.pack(side=LEFT)

        jump_btn = Button(bottom_frame, text="Jump", command=self.jump)
        jump_btn.pack(side=LEFT)

        label_expected = Label(bottom_frame, text="Expecting:")
        label_expected.pack(side=LEFT)

        entry_expected = Entry(bottom_frame, textvariable=self.expected_string)
        entry_expected.pack(side=LEFT)

        label_predicted = Label(bottom_frame, text="Predicted:")
        label_predicted.pack(side=LEFT)

        entry_predicted = Entry(bottom_frame, textvariable=self.predicted_string)
        entry_predicted.pack(side=LEFT)

        next_btn = Button(bottom_frame, text="Next", command=self.go_next)
        next_btn.pack(side=RIGHT)
        return

    def cmd_retrain(self):
        # import our Classifier avalaible
        from sklearn.svm import SVC
        # Create a classifier: a support vector classifier
        gamma = self.gamma_entry.get()

        if gamma.lower() == "auto":
            classifier = SVC()
        else:
            float_gamma = 0
            try:
                float_gamma = float(gamma)
            except:
                float_gamma = 0
            classifier = SVC(gamma=float_gamma)
            self.gamma_string.set(str(gamma))

        # turn the data in a (samples, feature) matrix:
        n_samples = len(self.digits.images)
        data = self.digits.images.reshape((n_samples, -1))
        # We train our model with the first half of data
        classifier.fit(data[:n_samples // 2], self.digits.target[:n_samples // 2])

        self.expected = self.digits.target[n_samples // 2:]
        self.predicted = classifier.predict(data[n_samples // 2:])

        self.nav_index = 0
        self.draw_digit(self.nav_index)
        return

    def go_pre(self):
        if self.nav_index >= 1:
            self.nav_index -= 1
        self.draw_digit(self.nav_index)
        return

    def go_next(self):
        n_samples = len(self.digits.images)
        if self.nav_index > n_samples // 2:
            return
        else:
            self.nav_index += 1
            self.draw_digit(self.nav_index)
        return

    def jump(self):
        target = int(self.index_string.get())
        n_samples = len(self.digits.images)
        if 0 <= target <= n_samples:
            self.nav_index = target
            self.draw_digit(self.nav_index)
        return

    @staticmethod
    def color_code(f):
        gray_level = 16-int(f)
        if gray_level <= 0:
            return "#000000"
        if gray_level >= 16:
            return "#ffffff"
        h = hex(gray_level*16+gray_level)
        c = '#'+h[2:]+h[2:]+h[2:]
        return c

    def draw_digit(self, index):
        n_samples = len(self.digits.images)
        if index > n_samples:
            return
        img_index = n_samples // 2 + index
        img = self.digits.images[img_index]
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                self.bitmap_block[row][col].configure(bg=self.color_code(img[row][col]))

        self.index_string.set(str(index))
        self.expected_string.set(str(self.expected[index]))
        self.predicted_string.set(str(self.predicted[index]))
        return


if __name__ == '__main__':
    app = MainWindow()
    app.cmd_retrain()
    app.run()
