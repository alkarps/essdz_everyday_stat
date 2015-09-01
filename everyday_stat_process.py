# -*- coding: utf8 -*-
__author__ = 'work';

import utils;

def formatStat(dicTable, setting):
    import Logger;
    try:
        login = setting[0];
        password = setting[1];
        host = setting[2];
        port = setting[3];
        sid = setting[4];
        servicename = setting[5];
        name = setting[6];
        Logger.info("Start formatting zubaTable for " + name);
        result = [];
        # Собирание строки для таблицы Зубарева
        listQueryForZubaTable = ["""select nvl(sum(decode(processingstatus, 'S', 1, 0)),0) "Success",
            nvl(sum(decode(processingstatus, 'E', 1, 0)),0) "Error",
            nvl(sum(decode(processingstatus, 'W', 1, 0)),0) "Wait",
            nvl(sum(decode(processingstatus, 'D', 1, 0)),0) "Deleted"
            from mdm_events where processingstatus !='N' and lastprocessingtime between trunc(SYSDATE-1,'HH24') and trunc(SYSDATE,'HH24') -1/86400""",
            """select count(1) "New_all" from mdm_events where operationtime between trunc(SYSDATE-1,'HH24') and trunc(SYSDATE,'HH24') -1/86400""",
            """select count(1) "New_processed" from mdm_events where operationtime between trunc(SYSDATE-1,'HH24') and trunc(SYSDATE,'HH24') -1/86400 and lastprocessingtime  between trunc(SYSDATE-1,'HH24') and trunc(SYSDATE,'HH24') -1/86400""",
            """select count(1) "All_processed" from mdm_events where lastprocessingtime  between trunc(SYSDATE-1,'HH24') and trunc(SYSDATE,'HH24') -1/86400"""];
        zubaRowTable = utils.getOneRowTableByListQuery(login, password, host, port, sid, servicename, listQueryForZubaTable, name);
        result.append(zubaRowTable);
        Logger.info("Start formatting errorTables for " + name);
        # Собирание таблицы статистики ошибок
        query = """SELECT  e.entitytypeid, me.name, e.operationtype, e.processingstatus, e.error_descr, count(*)
        FROM mdm_events e join mdm_entities me on e.entitytypeid=me.entitytypeid
        where e.entitytypeid not in (122,117,118,119,125,126,128) and e.processingstatus = 'E' and
        e.LASTPROCESSINGTIME BETWEEN trunc(SYSDATE-1,'HH24') and trunc(SYSDATE,'HH24')-1/86400
        group by e.entitytypeid, me.name, e.operationtype, e.processingstatus, e.error_descr order by e.entitytypeid, e.operationtype, e.processingstatus"""
        statTables = utils.getResultByQuery(login, password, host, port, sid, servicename, query);
        mdmError = """<table><tr><th>ID сущности</th><th>Название сущности</th><th>Операция</th><th>Статус</th><th>Описание ошибки</th><th>Количество</th></tr>""";
        mdmProxyError = """<table><tr><th>ID сущности</th><th>Название сущности</th><th>Операция</th><th>Статус</th><th>Описание ошибки</th><th>Количество</th></tr>""";
        asrError = """<table><tr><th>ID сущности</th><th>Название сущности</th><th>Операция</th><th>Статус</th><th>Описание ошибки</th><th>Количество</th></tr>""";
        for row in statTables:
            tmp = '<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td><td>{5}</td></tr>'.format(str(row[0]),str(row[1]),str(row[2]),str(row[3]),str(row[4]),str(row[5]));
            if 'ASRAdapter' in row[4]:
                asrError+=tmp;
            elif 'MDMPROXY' in row[4]:
                mdmProxyError+=tmp;
            else:
                mdmError+=tmp;
        mdmError += '</table>';
        mdmProxyError += '</table>';
        asrError += '</table>';
        stat = '<h2>' + name + '</h2>' + '</br>' + '<h2> MDM error </h2>' + mdmError + '<h2> MDMProxy error </h2>' + mdmProxyError + '<h2> ASRAdapter error </h2>' + asrError;
        result.append(stat);
        Logger.info("Add to dic for " + name);
        # Передача в основной поток
        if tuple(result) not in dicTable: dicTable[name] = tuple(result);
        Logger.info("Finish getESSDZStatByTNS for " + name);
    except Exception, exc:
        Logger.log.error("Fail getESSDZStatByTNS: %s" % str(exc));