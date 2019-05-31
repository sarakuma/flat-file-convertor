from flask import Flask, render_template, request, redirect, url_for, send_from_directory, send_file, flash
from werkzeug.utils import secure_filename
import json
from xlsxwriter import Workbook
import pandas as pd
import csv
import os
import lxml
from threading import Thread


# declare global vars
cur_val = 0
max_val = 100
trsfrm_no = 0
progress = []


def main():
    """main function that instantiates a flask app and handles payload"""

    # instantiate flask app
    app = Flask(__name__)

    # configure upload & download folders
    UPLOAD_FOLDER = './uploads'
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

    DOWNLOAD_FOLDER = './downloads'
    app.config["DOWNLOAD_FOLDER"] = DOWNLOAD_FOLDER

    # serve homepage and handle post request
    @app.route("/", methods=["GET", "POST"])
    def process_home_page():

        """ function to serve home page and handle post requests from home page"""

        global trsfrm_no, cur_val, max_val, progress

        if request.method == "GET":

            return render_template("index.html")

        elif request.method == "POST":

            trsfrm_no += 1

            if request.form["init-choice"] == "dtod":

                srcfil_object = request.files["infil"]
                srcfil_name = srcfil_object.filename
                sfilname = secure_filename(srcfil_name)

                srcfil_delim = request.form["indelim"]
                destfil_delim = request.form["outdelim"]

                if srcfil_delim == "csv":
                    srcfil_delim_char = ","
                elif srcfil_delim == "tsv":
                    srcfil_delim_char = r"\t"
                elif srcfil_delim == "psv":
                    srcfil_delim_char = "|"
                elif srcfil_delim == "~sv":
                    srcfil_delim_char = "~"

                name, _ = sfilname.split(".")

                if destfil_delim == "csv":
                    destfil_delim_char = ","
                    dest_fname = f"{name}.csv"
                elif destfil_delim == "tsv":
                    destfil_delim_char = "\t"
                    dest_fname = f"{name}.txt"
                elif destfil_delim == "psv":
                    destfil_delim_char = "|"
                    dest_fname = f"{name}.txt"
                elif destfil_delim == "~sv":
                    destfil_delim_char = "~"
                    dest_fname = f"{name}.txt"

                # create progress object
                trsfrm = {}
                trsfrm[trsfrm_no] = {"filename": dest_fname, "currVal": cur_val, "maxVal": max_val}
                progress.append(trsfrm)

                # save the uploaded file in upload directory
                srcfil_object.save(os.path.join(app.config["UPLOAD_FOLDER"], sfilname))

                thread = Thread(target=convert_to_another_delimited_file,
                                args=(app, trsfrm_no, sfilname, srcfil_delim_char, dest_fname, destfil_delim_char,))
                thread.start()

            elif request.form["init-choice"] == "dtoexcel":

                srcfil_object = request.files["infil"]
                srcfil_name = srcfil_object.filename

                srcfil_delim = request.form["indelim"]
                sfilname = secure_filename(srcfil_name)

                if srcfil_delim == "csv":
                    srcfil_delim_char = ","
                elif srcfil_delim == "tsv":
                    srcfil_delim_char = r"\t"
                elif srcfil_delim == "psv":
                    srcfil_delim_char = "|"
                elif srcfil_delim == "~sv":
                    srcfil_delim_char = "~"

                name, _ = sfilname.split(".")
                dest_fname = f"{name}.xlsx"
                temp_fname = f"{name}_temp.xlsx"

                # create progress object
                trsfrm = {}
                trsfrm[trsfrm_no] = {"filename": dest_fname, "currVal": cur_val, "maxVal": max_val}
                progress.append(trsfrm)

                # save the uploaded file in upload directory
                srcfil_object.save(os.path.join(app.config["UPLOAD_FOLDER"], sfilname))

                thread = Thread(target=convert_to_an_excel_sheet,
                                args=(app, trsfrm_no, sfilname, srcfil_delim_char, dest_fname, temp_fname,))
                thread.start()

            return render_template("download.html", progress=progress)

    # get the progress of file download
    @app.route("/download/progress/<transfer>", methods=["GET"])
    def get_current_download_progress(transfer):

        """ function to get the current progress of the file download  """

        global progress

        for inst in progress:
            if transfer in inst:
                break

        data = json.dumps(inst)

        return data

    # return transformed file after transformation
    @app.route("/download-file/<filename>")
    def download_file(filename):

        """ function to return the transformed file back to client as an attachment"""

        return send_from_directory(app.config["DOWNLOAD_FOLDER"], filename, as_attachment=True)

    app.run(host="localhost", port=9001, debug=True)

    return


def convert_to_another_delimited_file(app, trsfrm_no, sfilname, srcfil_delim_char, dest_fname, destfil_delim_char):
    """ function to convert inbound delimited file to requested delimited file    """

    global progress

    # #delete files found in download directory
    # for dirpath, dirname, files in os.walk(app.config["DOWNLOAD_FOLDER"]):
    #     print(dirpath, dirname, files)
    #     for filename in files:
    #         try:
    #             os.remove(os.path.join(dirpath, filename))
    #         except Exception as e:
    #             print(str(e))

    # read the uploaded file into pandas dff
    # use pandas to_csv method transform the file and save it to download directory
    dest_file = os.path.join(app.config["DOWNLOAD_FOLDER"], dest_fname)

    src_file = os.path.join(app.config["UPLOAD_FOLDER"], sfilname)

    with open(src_file, mode="r") as filhdlr:
        for idx, _ in enumerate(filhdlr):
            pass

    total_rows = idx + 1

    percent_1 = False
    percent_5 = False
    percent_10 = False
    percent_20 = False
    percent_30 = False
    percent_40 = False
    percent_50 = False
    percent_60 = False
    percent_70 = False
    percent_80 = False
    percent_90 = False
    percent_100 = False

    chunksize = 100000
    idx1 = 0

    for _, srcfil_df in enumerate(
            pd.read_csv(os.path.join(app.config["UPLOAD_FOLDER"], sfilname), index_col=None, header=None, dtype=object,
                        sep=srcfil_delim_char, chunksize=chunksize)):
        srcfil_df.to_csv(dest_file, sep=destfil_delim_char, index=None, mode="a+", header=None)

        # find the size of the dest file
        idx1 += 1
        idx1 = idx1 * chunksize
        percent_1, percent_5, percent_10, percent_20, percent_30, percent_40, percent_50, \
        percent_60, percent_70, percent_80, percent_90, percent_100 = determine_progress_value(idx1, total_rows,
                                                                                               percent_1, percent_5,
                                                                                               percent_10, percent_20,
                                                                                               percent_30, percent_40,
                                                                                               percent_50, \
                                                                                               percent_60, percent_70,
                                                                                               percent_80, percent_90,
                                                                                               percent_100)

    for idx2, inst in enumerate(progress):
        if trsfrm_no in inst.keys():
            progress[idx2][trsfrm_no]["currVal"] = 100

    # delete the uploaded file
    try:
        os.remove(os.path.join(app.config["UPLOAD_FOLDER"], sfilname))
    except Exception as e:
        print(str(e))

    return


def convert_to_an_excel_sheet(app, trsfrm_no, sfilname, srcfil_delim_char, dest_fname, temp_fname):
    """ function to convert inbound delimited file to an excel sheet """

    global progress

    # #delete files found in download directory
    # for dirpath, dirname, files in os.walk(app.config["DOWNLOAD_FOLDER"]):
    #     print(dirpath, dirname, files)
    #     for filename in files:
    #         try:
    #             os.remove(os.path.join(dirpath, filename))
    #         except Exception as e:
    #             print(str(e))

    dest_file = os.path.join(app.config["DOWNLOAD_FOLDER"], dest_fname)
    dest_wb = Workbook(dest_file, {'strings_to_numbers': True, 'constant_memory': True})
    sheet_name = f"file1"
    dest_ws = dest_wb.add_worksheet(name=sheet_name)

    src_file = os.path.join(app.config["UPLOAD_FOLDER"], sfilname)

    with open(src_file, mode="r") as filhdlr:
        for idx, _ in enumerate(filhdlr):
            pass

    total_rows = idx + 1

    percent_1 = False
    percent_5 = False
    percent_10 = False
    percent_20 = False
    percent_30 = False
    percent_40 = False
    percent_50 = False
    percent_60 = False
    percent_70 = False
    percent_80 = False
    percent_90 = False
    percent_100 = False

    with open(src_file, mode="r") as filhdlr:
        csvReader = csv.reader(filhdlr, delimiter=srcfil_delim_char)
        for idx1, row in enumerate(csvReader):

            percent_1, percent_5, percent_10, percent_20, percent_30, percent_40, percent_50, \
            percent_60, percent_70, percent_80, percent_90, percent_100 = determine_progress_value(idx1, total_rows,
                                                                                                   percent_1, percent_5,
                                                                                                   percent_10,
                                                                                                   percent_20,
                                                                                                   percent_30,
                                                                                                   percent_40,
                                                                                                   percent_50, \
                                                                                                   percent_60,
                                                                                                   percent_70,
                                                                                                   percent_80,
                                                                                                   percent_90,
                                                                                                   percent_100)

            for idx2, value in enumerate(row):
                dest_ws.write(idx1, idx2, value)

    dest_wb.close()

    for idx2, inst in enumerate(progress):
        if trsfrm_no in inst.keys():
            progress[idx2][trsfrm_no]["currVal"] = 100

    # delete the uploaded file
    try:
        os.remove(os.path.join(app.config["UPLOAD_FOLDER"], sfilname))
    except Exception as e:
        print(str(e))

    return


def determine_progress_value(rows, total_rows, percent_1, percent_5, percent_10, percent_20, percent_30, percent_40,
                             percent_50,
                             percent_60, percent_70, percent_80, percent_90, percent_100):
    """ function to determine the progress value during file download """

    if rows >= total_rows * 1.0 and not percent_100:
        for idx2, inst in enumerate(progress):
            if trsfrm_no in inst.keys():
                progress[idx2][trsfrm_no]["currVal"] = 100
        percent_100 = True
    elif rows >= total_rows * 0.9 and not percent_90:
        for idx2, inst in enumerate(progress):
            if trsfrm_no in inst.keys():
                progress[idx2][trsfrm_no]["currVal"] = 90
        percent_90 = True
    elif rows >= total_rows * 0.8 and not percent_80:
        for idx2, inst in enumerate(progress):
            if trsfrm_no in inst.keys():
                progress[idx2][trsfrm_no]["currVal"] = 80
        percent_80 = True
    elif rows >= total_rows * 0.7 and not percent_70:
        for idx2, inst in enumerate(progress):
            if trsfrm_no in inst.keys():
                progress[idx2][trsfrm_no]["currVal"] = 70
        percent_70 = True
    elif rows >= total_rows * 0.6 and not percent_60:
        for idx2, inst in enumerate(progress):
            if trsfrm_no in inst.keys():
                progress[idx2][trsfrm_no]["currVal"] = 60
        percent_60 = True
    elif rows >= total_rows * 0.5 and not percent_50:
        for idx2, inst in enumerate(progress):
            if trsfrm_no in inst.keys():
                progress[idx2][trsfrm_no]["currVal"] = 50
        percent_50 = True
    elif rows >= total_rows * 0.4 and not percent_40:
        for idx2, inst in enumerate(progress):
            if trsfrm_no in inst.keys():
                progress[idx2][trsfrm_no]["currVal"] = 40
        percent_40 = True
    elif rows >= total_rows * 0.3 and not percent_30:
        for idx2, inst in enumerate(progress):
            if trsfrm_no in inst.keys():
                progress[idx2][trsfrm_no]["currVal"] = 30
        percent_30 = True
    elif rows >= total_rows * 0.2 and not percent_20:
        for idx2, inst in enumerate(progress):
            if trsfrm_no in inst.keys():
                progress[idx2][trsfrm_no]["currVal"] = 20
        percent_20 = True
    elif rows >= total_rows * 0.1 and not percent_10:
        for idx2, inst in enumerate(progress):
            if trsfrm_no in inst.keys():
                progress[idx2][trsfrm_no]["currVal"] = 10
        percent_10 = True
    elif rows >= total_rows * 0.05 and not percent_5:
        for idx2, inst in enumerate(progress):
            if trsfrm_no in inst.keys():
                progress[idx2][trsfrm_no]["currVal"] = 5
        percent_5 = True
    elif rows >= total_rows * 0.01 and not percent_1:
        for idx2, inst in enumerate(progress):
            if trsfrm_no in inst.keys():
                progress[idx2][trsfrm_no]["currVal"] = 1
        percent_1 = True

    return percent_1, percent_5, percent_10, percent_20, percent_30, percent_40, percent_50, percent_60, percent_70, percent_80, percent_90, percent_100


if __name__ == "__main__":
    main()