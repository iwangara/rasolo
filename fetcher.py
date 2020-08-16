import requests
import db
import config


sql = db.DBManager()
BASE_URL=config.BASE_URL


def fetch_africa(language):
    url = f"{BASE_URL}solo/africa/{language}"
    africas = requests.get(url=url).json()
    if len(africas)>0:
        for africa in africas:
            africa_id = africa['id']
            africa_language = africa['language']
            africa_question = africa['question']
            africa_answer = africa['answer1']
            africa_answer1 = africa['answer1']
            africa_answer2 = africa['answer2']
            africa_answer3 = africa['answer3']
            africa_answer4 = africa['answer4']
            africa_level = africa['level']
            sql.save_africa(quesId=africa_id, question=africa_question, answer=africa_answer,
                            answer1=africa_answer1, answer2=africa_answer2, answer3=africa_answer3,
                            answer4=africa_answer4,
                            qlevel=africa_level, qlanguage=africa_language)
    else:
        return False


def fetch_apollo(language):
    url = f"{BASE_URL}solo/apollo/{language}"
    apollos = requests.get(url=url).json()
    if len(apollos) > 0:
        for apollo in apollos:
            apollo_id = apollo['id']
            apollo_language = apollo['language']
            apollo_question = apollo['question']
            apollo_answer = apollo['answer']

            apollo_level = apollo['level']
            sql.save_apollo(quesId=apollo_id, question=apollo_question, answer=apollo_answer,
                            qlevel=apollo_level, qlanguage=apollo_language)
    else:
        return False

def fetch_gaia(language):
    url = f"{BASE_URL}solo/gaia/{language}"
    gaias = requests.get(url=url).json()
    if len(gaias) > 0:
        for gaia in gaias:
            gaia_id = gaia['id']
            gaia_language = gaia['language']
            gaia_answer = gaia['question']
            gaia_level = gaia['level']
            gaia_question = gaia['path']
            sql.save_gaia(quesId=gaia_id, question=gaia_question, answer=gaia_answer,
                            qlevel=gaia_level, qlanguage=gaia_language)
    else:
        return False


def fetch_kadlu(language):
    url = f"{BASE_URL}solo/kadlu/{language}"
    kadlus = requests.get(url=url).json()
    if len(kadlus) > 0:
        for kadlu in kadlus:
            kadlu_id = kadlu['id']
            kadlu_language = kadlu['language']
            kadlu_main_id = kadlu['sub_question_id']
            kadlu_main_question = kadlu['path']
            kadlu_question = kadlu['sub_question']
            kadlu_answer = kadlu['answer1']
            kadlu_answer1 = kadlu['answer1']
            kadlu_answer2 = kadlu['answer2']
            kadlu_answer3 = kadlu['answer3']
            kadlu_answer4 = kadlu['answer4']
            kadlu_level = 'Elementary'
            sql.save_kadlu(quesId=kadlu_id, main_id=kadlu_main_id, main_question=kadlu_main_question,question=kadlu_question, answer=kadlu_answer, answer1=kadlu_answer1, answer2=kadlu_answer2, answer3=kadlu_answer3, answer4=kadlu_answer4, qlevel=kadlu_level, qlanguage=kadlu_language )
    else:
        return False


def fetch_leizi(language):
    url = f"{BASE_URL}solo/leizi/{language}"
    leizis = requests.get(url=url).json()
    if len(leizis) > 0:
        for leizi in leizis:
            leizi_id = leizi['id']
            leizi_language = leizi['language']
            leizi_question = leizi['question']
            leizi_answer1 = leizi['answer1']
            leizi_answer2 = leizi['answer2']
            leizi_instruction = leizi['instruction']
            leizi_level = leizi['level']
            sql.save_leizi(quesId=leizi_id, question=leizi_question, answer1=leizi_answer1, answer2=leizi_answer2, instruction=leizi_instruction, qlevel=leizi_level, qlanguage=leizi_language )
    else:
        return False


def fetch_nuwa(language):
    url = f"{BASE_URL}solo/nuwa/{language}"
    nuwas = requests.get(url=url).json()
    if len(nuwas) > 0:
        for nuwa in nuwas:
            nuwa_id = nuwa['id']
            nuwa_language = nuwa['language']
            nuwa_question = nuwa['question']
            nuwa_level = nuwa['level']
            sql.save_nuwa(quesId=nuwa_id, question=nuwa_question,qlevel=nuwa_level, qlanguage=nuwa_language)

    else:
        return False

def fetch_odin(language):
    url = f"{BASE_URL}solo/odin/{language}"
    odins = requests.get(url=url).json()
    if len(odins) > 0:
        for odin in odins:
            odin_id = odin['id']
            odin_language = odin['language']
            odin_question = odin['question']
            odin_meaning = odin['meaning']
            odin_level = odin['level']
            sql.save_odin(quesId=odin_id, question=odin_question,meaning=odin_meaning,qlevel=odin_level, qlanguage=odin_language)

    else:
        return False


def fetch_seshat(language):
    url = f"{BASE_URL}solo/seshat/{language}"
    seshats = requests.get(url=url).json()
    if len(seshats) > 0:
        for seshat in seshats:
            seshat_id = seshat['id']
            seshat_language = seshat['language']
            seshat_question = seshat['question']
            seshat_answer = seshat['answer']
            seshat_instruction = seshat['instruction']
            seshat_level = seshat['level']
            seshat_gif = seshat['img']
            sql.save_seshat(quesId=seshat_id, question=seshat_question,answer=seshat_answer,instruction=seshat_instruction,gif=seshat_gif,qlevel=seshat_level, qlanguage=seshat_language)

    else:
        return False


def fetch_tyche(language):
    url = f"{BASE_URL}solo/tyche/{language}"
    tyches = requests.get(url=url).json()
    if len(tyches) > 0:
        for tyche in tyches:
            tyche_id = tyche['id']
            tyche_language = tyche['language']
            tyche_question = tyche['hint']
            tyche_answer = tyche['question']
            tyche_level = tyche['level']
            sql.save_tyche(quesId=tyche_id, question=tyche_question,answer=tyche_answer,qlevel=tyche_level, qlanguage=tyche_language)

    else:
        return False

def fetch_wala(language):
    url = f"{BASE_URL}solo/wala/{language}"
    walas = requests.get(url=url).json()
    if len(walas) > 0:
        for wala in walas:
            wala_id = wala['id']
            wala_language = wala['language']
            wala_main_id = wala['sub_question_id']
            wala_main_question = wala['main_question']
            wala_question = wala['sub_question']
            wala_answer = wala['answer1']
            wala_answer1 = wala['answer1']
            wala_answer2 = wala['answer2']
            wala_answer3 = wala['answer3']
            wala_answer4 = wala['answer4']
            wala_level = 'Elementary'
            sql.save_wala(quesId=wala_id, main_id=wala_main_id, main_question=wala_main_question,question=wala_question, answer=wala_answer, answer1=wala_answer1, answer2=wala_answer2, answer3=wala_answer3, answer4=wala_answer4, qlevel=wala_level, qlanguage=wala_language )
    else:
        return False


def fetch_zamo(language):
    url = f"{BASE_URL}solo/zamo/{language}"
    zamos = requests.get(url=url).json()
    if len(zamos) > 0:
        for zamo in zamos:
            zamo_id = zamo['id']
            zamo_language = zamo['language']
            zamo_question = zamo['path']
            zamo_answer = zamo['question']

            zamo_level = zamo['level']
            sql.save_zamo(quesId=zamo_id, question=zamo_question, answer=zamo_answer,
                            qlevel=zamo_level, qlanguage=zamo_language)
    else:
        return False