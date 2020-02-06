import sys
import csv
from datetime import datetime
from PyQt5 import QtWidgets
from main import Ui_Dialog
from PyQt5.QtWidgets import QProgressDialog, QMessageBox, QWidget, QDialogButtonBox, QVBoxLayout, QPushButton
from fileobj import FileObj

INPUT_PATH = 'input/'
OUT_PATH = 'output/'

class DataConvert(Ui_Dialog):

    data = []
    filtered_data = []

    columns = []
    input_filename = 'contribs_01.csv'
    filter_format = ''
    filter_column_name = ''
    filter_column_index = 0
    start_value = ''
    end_value = ''
    selected_rows = 0
    output_filename = ''

    def __init__(self, dialog):
        Ui_Dialog.__init__(self)
        self.setupUi(dialog)
        # self.config(dialog)

        self.browser.clicked.connect(self.input_filename_browser_clicked)
        self.importBtn.clicked.connect(self.input_filename_import_clicked)
        self.filterFormat.currentIndexChanged.connect(self.filter_format_changed)
        self.filterBtn.clicked.connect(self.filter_button_clicked)
        self.saveBtn.clicked.connect(self.csv_save_clicked)

        # self.filterColunm.dropEvent(self.make_filter_columns)

    def csv_save_clicked(self):
        output_filename = self.outputFileName.text()
        if output_filename == '':
            self.alertMessage('Please enter a output file name!')
            return False
        with open(OUT_PATH + output_filename + '.csv', 'w', newline='') as file:
            output = csv.writer(file, delimiter=',')
            output.writerow(self.columns)
            output.writerows(self.filtered_data)
            file.close()
        self.alertMessage('Success!')
        print('success')

    def filter_button_clicked(self):

        filtered_data = []

        start_value = self.startValue.text()
        end_value = self.endValue.text()
        column_index = self.filterColunm.currentIndex()
        format_index = self.filterFormat.currentIndex()
        print(start_value)
        print(end_value)

        # try:
        for row in self.data:
            cell_value = row[column_index]
            if format_index == 0:
                try:
                    cell_value = float(cell_value)
                except:
                    self.alertMessage('There is a non-numeric value in the selected column.')
                    return False

                if start_value != '':
                    try:
                        start_value = float(start_value)
                    except:
                        self.alertMessage('Start Value must be numeric.')
                        return False
                if end_value != '':
                    try:
                        end_value = float(end_value)
                    except:
                        self.alertMessage('End Value must be numeric.')
                        return False
                if start_value == '' and end_value == '':
                    filtered_data = self.data
                    break
                elif start_value == '' and cell_value > end_value:

                    continue
                elif end_value == '' and cell_value < start_value:
                    continue
                elif start_value != '' and end_value != '':
                    if cell_value < start_value or cell_value > end_value:
                        continue

            elif format_index == 1:
                if cell_value != start_value:
                    continue
            else:
                if cell_value.find(start_value) == -1:
                    continue
            filtered_data.append(row)
        self.filtered_data = filtered_data
        # except:
        #     self.alertMessage('Filter Error!')
        #     return False
        print(str(len(self.filtered_data)))
        self.selectedRows.setText(str(len(self.filtered_data)))
        return True


    def filter_format_changed(self):
        if self.filterFormat.currentIndex() != 0:
            self.endValue.setDisabled(True)
        else:
            self.endValue.setDisabled(False)


    def input_filename_import_clicked(self):
        input_filename = self.inputFileName.text()
        columns = []
        data = []
        try:
            with open(input_filename, 'r') as file:
                reader = csv.reader(file, delimiter=',')
                row_num = 0
                start_time = datetime.now()
                for row in reader:
                    if row_num == 0:
                        if row[0].find(',') >= 0:
                            columns = row[0].split(',')
                        else:
                            columns = row
                    else:
                        if row[0].find(',') >= 0:
                            cell_array = row[0].split(',')
                        else:
                            cell_array = row

                        data.append(cell_array)

                    row_num = row_num + 1
                end_time = datetime.now()
                print(end_time - start_time)
        except:
            self.alertMessage("Can't read the csv file! Please input a correct csv file.")
            return False
        if len(columns) == 0:
            self.alertMessage("Columns Empty! Please input a correct csv file.")
            return False

        self.make_filter_columns(columns)

        self.input_filename = input_filename
        if len(input_filename) > 50:
            input_filename = input_filename[0:20] + ' ... ' + input_filename[-25:]
        self.importedCsvFile.setText(input_filename)
        self.data = data
        print(data[0])
        self.selectedRows.setText(str(len(self.data)))

        return True

    def make_filter_columns(self, columns):
        self.filterColunm.clear()
        print(columns)
        for column in columns:
            self.filterColunm.addItem(column)
        self.columns = columns
        return True

    def input_filename_browser_clicked(self):
        fileObj = FileObj()
        inputCsv = fileObj.openFileNameDialog()
        print('Csv: ', inputCsv)
        self.inputFileName.setText(inputCsv)

    def alertMessage(self, message):
        message = message + '        '
        msgBox = QMessageBox()
        # msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(message)
        msgBox.setWindowTitle("Note!")
        msgBox.setStandardButtons(QMessageBox.Ok)
        returnValue = msgBox.exec()

    def get_data_from_csv(self):
        with open(INPUT_PATH + self.input_filename, 'r') as file:
            reader = csv.reader(file, delimiter=',')
            row_num = 0
            start_time = datetime.now()
            for row in reader:
                cell_array = []
                if row_num == 0:
                    # print(len(row))
                    self.columns = row
                else:
                    cell_array = row[0].split(',')
                    self.data.append(cell_array)

                row_num = row_num + 1
            end_time = datetime.now()
            print(end_time - start_time)
        return True

    def get_data_by_filter(self, col_name, option, start_value, end_value):
        col_num = self.columns.index(col_name)
        for row in self.data:
            cell_val = row[col_num]
            if option == 'like':
                filter_val = start_value
                if cell_val.find(filter_val) < 0:
                    continue
            elif option == 'same':
                filter_val = start_value
                if cell_val != filter_val:
                    continue
            elif option == '<>':
                if cell_val < start_value:
                    continue
                if cell_val > end_value:
                    continue
            self.filtered_data.append(row)
        return len(self.filtered_data)


def main():

    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    dataConvert = DataConvert(dialog)
    dialog.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()