# -*- coding: utf8 -*-
__author__ = 'work';

if __name__ == '__main__':
    from multiprocessing import Process, Manager;
    import mail;
    import everyday_stat_settingfile as sf;
    import everyday_stat_process as proc;
    import Logger;
    Logger.initLogger(sf.name_logfile, sf.logger_name)
    Logger.info("Start formatting statistic");
    manager = Manager();
    dicTable = manager.dict();
    processList = [];
    Logger.info("Start threads");
    for setting in sf.start_connect_param:
        process = Process(target=proc.formatStat, args=(dicTable, setting));
        processList.append(process);
        process.start();
    for process in processList:
        process.join();
    Logger.info("Finish threads");
    Logger.info("Start building text mail");
    emailText = """<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <title>ЕССДЗ Статистика</title>
        <style type="text/css">
            table {
                border-collapse: collapse;
            }
            th {
                background: #ccc;
                text-align: center;
            }
            td{
                text-align: right;
            }
            td, th {
                border: 1px solid #800;
                padding: 4px;
            }
        </style>
    </head>
        <body>
            <table style="border-collapse: collapse;">
                <tr>
                    <th rowspan="2">RF</th>
                    <th rowspan="2">Success</th>
                    <th rowspan="2">Error</th>
                    <th rowspan="2">Wait</th>
                    <th rowspan="2">Deleted</th>
                    <th colspan="2">New</th>
                    <th rowspan="2">All processed</th>
                </tr>
                <tr>
                    <th>all</th>
                    <th>processed</th>
                </tr>""";
    keys = dicTable.keys();
    errorTables = "";
    for key in keys:
        emailText = emailText + dicTable[key][0];
        errorTables += dicTable[key][1] + "<br>";
    emailText += "</table>\n" + errorTables + "</body></html>";
    Logger.info("Finish building text mail");
    if(len(dicTable)!=0):
        Logger.info("Start sending mail");
        mail.sent_mail(text=emailText, to=sf.to, subj=sf.subject, toView=sf.toView);
        Logger.info("Finish sending mail");