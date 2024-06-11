import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class Analysis:
    def __init__(self):
        pass

    def plot_score(self, score_res):
        names = [item['name'] for item in score_res]
        scores = [item['score'] for item in score_res]
        bot_scores = [item['bot_score'] for item in score_res]
        
        width_bar = 0.4
        x = np.arange(len(names))
        x1 = x - width_bar / 2
        x2 = x + width_bar / 2

        fig, ax = plt.subplots(figsize=(20, 10))

        ax.set_xlabel('Games')
        ax.set_ylabel('Scores')

        ax.bar(x1, scores, width=width_bar, label='Our Model')
        ax.bar(x2, bot_scores, width=width_bar, label='llama3-70B Model')

        ax.set_xticks(x)
        ax.set_xticklabels(names, rotation=90)

        y_ticks = np.arange(0, 11, 1)
        custom_ticks = np.concatenate([y_ticks[:6], np.arange(6, 7.5, 0.5), y_ticks[7:]])
        ax.set_yticks(custom_ticks)
        plt.ylim(6,10.1)
        y_tick_labels = [str(tick) if tick in y_ticks else '' for tick in custom_ticks]
        ax.set_yticklabels(y_tick_labels)
        
        mean_score = np.mean(scores)
        mean_bot_score = np.mean(bot_scores)
        ax.axhline(y=mean_score, color='blue', linestyle='--', linewidth=1, label='Mean of Our Model Score')
        ax.axhline(y=mean_bot_score, color='red', linestyle='--', linewidth=1, label='Mean of llama3-70B Model Score')
        
        ax.legend()
        
        plt.title('Game Scores Comparison between Our Model and llama3-70B Model')
        plt.tight_layout()
        plt.show()
    
    def table_perf(self, perf_res):
        names = [item['name'] for item in perf_res]
        running_times = [item['running_time'] for item in perf_res]

        df = pd.DataFrame({
            'Game': names,
            'Running Time': running_times
        })

        print(df)

        mean_time = np.mean(running_times)
        min_time = np.min(running_times)
        max_time = np.max(running_times)

        summary_df = pd.DataFrame({
            'Metric': ['Mean Running Time', 'Min Running Time', 'Max Running Time'],
            'Value': [mean_time, min_time, max_time]
        })

        print("\nRunning time on GPU:")
        print(summary_df)

    def plot_cl_score(self, cl_list):
        names = [item['name'] for item in cl_list]
        cl_scores = [item['clscore'] for item in cl_list]

        fig, ax = plt.subplots(figsize=(20, 10))
        x = np.arange(len(names))

        ax.bar(x, cl_scores, color='blue', width=0.4)

        ax.set_xlabel('Games')
        ax.set_ylabel('CL Scores')
        ax.set_xticks(x)
        ax.set_xticklabels(names, rotation=90)
        plt.ylim(0, 11)

        plt.title('CL Scores of Games')
        plt.tight_layout()
        plt.show()
    
    def table_clscore(self, cl_list):
        names = [item['name'] for item in cl_list]
        cl_scores = [item['clscore'] for item in cl_list]

        df = pd.DataFrame({
            'Game': names,
            'CL Score': cl_scores
        })

        print(df)

        mean_cl_score = np.mean(cl_scores)
        min_cl_score = np.min(cl_scores)
        max_cl_score = np.max(cl_scores)

        summary_df = pd.DataFrame({
            'Metric': ['Mean CL Score', 'Min CL Score', 'Max CL Score'],
            'Value': [mean_cl_score, min_cl_score, max_cl_score]
        })

        print("\nCL Score Statistics:")
        print(summary_df)

    def printgames(self, games):
        df = pd.DataFrame({
            'Game': games
        })
        print(df)

score_list = [
    {'name': 'Forza Horizon 4', 'score': 8, 'bot_score': 8},
    {'name': 'The Witcher 3: Wild Hunt', 'score': 8, 'bot_score': 8},
    {'name': 'Cyberpunk 2077', 'score': 8, 'bot_score': 8},
    {'name': 'ELDEN RING', 'score': 8, 'bot_score': 10},
    {'name': 'Destiny 2', 'score': 8, 'bot_score': 8},
    {'name': 'Nine Sols', 'score': 9, 'bot_score': 9},
    {'name': 'Counter-Strike 2', 'score': 8, 'bot_score': 8},
    {'name': 'World of Tanks', 'score': 8, 'bot_score': 8},
    {'name': 'NARAKA: BLADEPOINT', 'score': 8, 'bot_score': 9},
    {'name': 'PUBG: BATTLEGROUNDS', 'score': 8, 'bot_score': 8},
    {'name': 'Left 4 Dead 2', 'score': 8, 'bot_score': 8},
    {'name': 'Half-Life 2', 'score': 8, 'bot_score': 9},
    {'name': 'ARK: Survival Evolved', 'score': 9, 'bot_score': 8},
    {'name': 'Among Us', 'score': 8, 'bot_score': 8},
    {'name': "Tom Clancy's Rainbow Six Siege", 'score': 8, 'bot_score': 8},
    {'name': 'DayZ', 'score': 7, 'bot_score': 8},
    {'name': 'FIFA 22', 'score': 9, 'bot_score': 8},
    {'name': 'NBA 2K24', 'score': 8, 'bot_score': 9},
    {'name': 'DEAD OR ALIVE Xtreme Venus Vacation', 'score': 8, 'bot_score': 9},
    {'name': 'Terraria', 'score': 9, 'bot_score': 10},
    {'name': 'Albion Online', 'score': 8, 'bot_score': 8},
    {'name': 'Need for Speed: Hot Pursuit', 'score': 9, 'bot_score': 9},
    {'name': 'Dead by Daylight', 'score': 9, 'bot_score': 8},
    {'name': 'Palworld', 'score': 8, 'bot_score': 8},
    {'name': 'Cities: Skylines II', 'score': 9, 'bot_score': 8},
    {'name': 'Hades II', 'score': 8, 'bot_score': 8},
    {'name': 'Yu-Gi-Oh!  Master Duel', 'score': 8, 'bot_score': 8},
    {'name': 'Undertale', 'score': 8, 'bot_score': 8},
    {'name': 'Fall Guys', 'score': 8, 'bot_score': 9},
    {'name': 'Geometry Dash', 'score': 7, 'bot_score': 8},
    {'name': 'Resident Evil Village', 'score': 9, 'bot_score': 8},
    {'name': 'Raft', 'score': 9, 'bot_score': 8},
    {'name': 'The Forest', 'score': 8, 'bot_score': 8},
    {'name': 'GUILTY GEAR -STRIVE-', 'score': 9, 'bot_score': 8},
    {'name': 'Warframe', 'score': 8, 'bot_score': 9},
    {'name': "Baldur's Gate 3", 'score': 9, 'bot_score': 8},
    {'name': 'Apex Legends', 'score': 8, 'bot_score': 8},
    {'name': 'Stardew Valley', 'score': 8, 'bot_score': 8},
    {'name': "Assassin's Creed Valhalla", 'score': 8, 'bot_score': 8},
    {'name': 'Hogwarts Legacy', 'score': 8, 'bot_score': 9},
    {'name': "Tom Clancy's The Division 2", 'score': 8, 'bot_score': 8},
    {'name': 'Halo Infinite', 'score': 9, 'bot_score': 9},
    {'name': 'Detroit: Become Human', 'score': 8, 'bot_score': 8},
]

cpu_time_list = [
    {'name': 'Forza Horizon 4', 'running_time': 88.07096433639526},
    {'name': 'The Witcher 3: Wild Hunt', 'running_time': 81.6439733505249},
    {'name': 'Cyberpunk 2077', 'running_time': 87.39216041564941},
    {'name': 'ELDEN RING', 'running_time': 76.09405326843262},
    {'name': 'Destiny 2', 'running_time': 77.13815665245056},
    {'name': 'Nine Sols', 'running_time': 134.75457906723022},
    {'name': 'Counter-Strike 2', 'running_time': 78.39325022697449},
    {'name': 'World of Tanks', 'running_time': 106.7906756401062},
    {'name': 'NARAKA: BLADEPOINT', 'running_time': 87.61852669715881},
    {'name': 'PUBG: BATTLEGROUNDS', 'running_time': 91.03572487831116},
    {'name': 'Left 4 Dead 2', 'running_time': 101.05147910118103},
    {'name': 'Half-Life 2', 'running_time': 82.61595320701599},
    {'name': 'ARK: Survival Evolved', 'running_time': 155.02908635139465},
    {'name': 'Among Us', 'running_time': 80.1296899318695},
    {'name': "Tom Clancy's Rainbow Six Siege", 'running_time': 74.07949686050415},
    {'name': 'DayZ', 'running_time': 74.51588416099548},
    {'name': 'FIFA 22', 'running_time': 137.96083235740662},
    {'name': 'NBA 2K24', 'running_time': 79.52840948104858},
    {'name': 'DEAD OR ALIVE Xtreme Venus Vacation', 'running_time': 82.94445466995239},
    {'name': 'Terraria', 'running_time': 105.59266829490662},
    {'name': 'Albion Online', 'running_time': 79.91973543167114},
    {'name': 'Need for Speed: Hot Pursuit', 'running_time': 92.52768778800964},
    {'name': 'Dead by Daylight', 'running_time': 92.1528172492981},
    {'name': 'Palworld', 'running_time': 111.79993915557861},
    {'name': 'Palworld', 'running_time': 111.79993915557861},
    {'name': 'Cities: Skylines II', 'running_time': 82.96658182144165},
    {'name': 'Hades II', 'running_time': 95.26996326446533},
    {'name': 'Yu-Gi-Oh!  Master Duel', 'running_time': 96.40641808509827},
    {'name': 'Undertale', 'running_time': 57.878711462020874},
    {'name': 'Fall Guys', 'running_time': 61.980507612228394},
    {'name': 'Geometry Dash', 'running_time': 66.4136073589325},
    {'name': 'Resident Evil Village', 'running_time': 78.14438724517822},
    {'name': 'Raft', 'running_time': 71.9981164932251},
    {'name': 'The Forest', 'running_time': 69.32988667488098},
    {'name': 'GUILTY GEAR -STRIVE-', 'running_time': 75.51534461975098},
    {'name': 'Warframe', 'running_time': 57.91894245147705},
    {'name': "Baldur's Gate 3", 'running_time': 71.3592426776886},
    {'name': 'Apex Legends', 'running_time': 78.68487286567688},
    {'name': 'Stardew Valley', 'running_time': 71.62657284736633},
    {'name': "Assassin's Creed Valhalla", 'running_time': 107.35537099838257},
    {'name': 'Hogwarts Legacy', 'running_time': 107.26717042922974},
    {'name': "Tom Clancy's The Division 2", 'running_time': 80.35185170173645},
    {'name': 'Halo Infinite', 'running_time': 84.04059910774231},
    {'name': 'Detroit: Become Human', 'running_time': 88.97667407989502},
]

cl_list = [
    {'name': 'Cyberpunk 2077', 'clscore': 10},
    {'name': 'ELDEN RING', 'clscore': 9},
    {'name': 'Nine Sols', 'clscore': 10},
    {'name': 'Counter-Strike 2', 'clscore': 8},
    {'name': 'World of Tanks', 'clscore': 10},
    {'name': 'NARAKA: BLADEPOINT', 'clscore': 7},
    {'name': 'PUBG: BATTLEGROUNDS', 'clscore': 7},
    {'name': 'Left 4 Dead 2', 'clscore': 10},
    {'name': 'ARK: Survival Evolved', 'clscore': 10},
    {'name': "Tom Clancy's Rainbow Six Siege", 'clscore': 10},
    {'name': 'FIFA 22', 'clscore': 4},
    {'name': 'DEAD OR ALIVE Xtreme Venus Vacation', 'clscore': 8},
    {'name': 'Terraria', 'clscore': 10},
    {'name': 'Need for Speed: Hot Pursuit', 'clscore': 7},
    {'name': 'Fall Guys', 'clscore': 8},
    {'name': 'The Forest', 'clscore': 10},
    {'name': 'GUILTY GEAR -STRIVE-', 'clscore': 10},
    {'name': "Baldur's Gate 3", 'clscore': 10},
    {'name': 'Apex Legends', 'clscore': 1},
    {'name': 'Stardew Valley', 'clscore': 7},
    {'name': "Assassin's Creed Valhalla", 'clscore': 10},
    {'name': 'Hogwarts Legacy', 'clscore': 8},
    {'name': "Tom Clancy's The Division 2", 'clscore': 10},
    {'name': 'Halo Infinite', 'clscore': 10},
    {'name': 'Detroit: Become Human', 'clscore': 7},
]

gpu_time_list = [
    {'name': 'Forza Horizon 4', 'running_time': 25.126774549484253},
    {'name': 'The Witcher 3: Wild Hunt', 'running_time': 12.98270058631897},
    {'name': 'Cyberpunk 2077', 'running_time': 7.701420307159424},
    {'name': 'ELDEN RING', 'running_time': 33.31486225128174},
    {'name': 'Destiny 2', 'running_time': 11.420680284500122},
    {'name': 'Nine Sols', 'running_time': 22.55233097076416},
    {'name': 'Counter-Strike 2', 'running_time': 10.581708192825317},
    {'name': 'World of Tanks', 'running_time': 17.170873165130615},
    {'name': 'NARAKA: BLADEPOINT', 'running_time': 32.22250056266785},
    {'name': 'PUBG: BATTLEGROUNDS', 'running_time': 19.882073402404785},
    {'name': 'Left 4 Dead 2', 'running_time': 16.165056467056274},
    {'name': 'Half-Life 2', 'running_time': 20.189919471740723},
    {'name': 'ARK: Survival Evolved', 'running_time': 20.894206523895264},
    {'name': 'Among Us', 'running_time': 13.206202983856201},
    {'name': "Tom Clancy's Rainbow Six Siege", 'running_time': 16.467744827270508},
    {'name': 'DayZ', 'running_time': 17.613887310028076},
    {'name': 'FIFA 22', 'running_time': 19.70681071281433},
    {'name': 'NBA 2K24', 'running_time': 15.03178095817566},
    {'name': 'DEAD OR ALIVE Xtreme Venus Vacation', 'running_time': 13.57611608505249},
    {'name': 'Terraria', 'running_time': 26.38991093635559},
    {'name': 'Albion Online', 'running_time': 24.628379344940186},
    {'name': 'Need for Speed: Hot Pursuit', 'running_time': 10.630838394165039},
    {'name': 'Dead by Daylight', 'running_time': 18.69794249534607},
    {'name': 'Palworld', 'running_time': 23.29098916053772},
    {'name': 'Cities: Skylines II', 'running_time': 20.55137586593628},
    {'name': 'Hades II', 'running_time': 10.204630613327026},
    {'name': 'Yu-Gi-Oh!  Master Duel', 'running_time': 6.142086744308472},
    {'name': 'Undertale', 'running_time': 22.1581609249115},
    {'name': 'Fall Guys', 'running_time': 12.503463745117188},
    {'name': 'Geometry Dash', 'running_time': 23.179686307907104},
    {'name': 'Resident Evil Village', 'running_time': 13.100373029708862},
    {'name': 'Raft', 'running_time': 12.977519273757935},
    {'name': 'The Forest', 'running_time': 20.04870867729187},
    {'name': 'GUILTY GEAR -STRIVE-', 'running_time': 9.83696961402893},
    {'name': 'Warframe', 'running_time': 15.415921688079834},
    {'name': "Baldur's Gate 3", 'running_time': 22.26060652732849},
    {'name': 'Apex Legends', 'running_time': 23.400609731674194},
    {'name': 'Stardew Valley', 'running_time': 10.991255283355713},
    {'name': "Assassin's Creed Valhalla", 'running_time': 13.316340208053589},
    {'name': 'Hogwarts Legacy', 'running_time': 11.248502254486084},
    {'name': "Tom Clancy's The Division 2", 'running_time': 26.276017904281616},
    {'name': 'Halo Infinite', 'running_time': 19.282024383544922},
    {'name': 'Detroit: Become Human', 'running_time': 14.412535429000854},
]

tf_idf_list = [
   {'name': 'Detroit: Become Human', 'our_idf_evaluate': 0.23, 'bot_idf_evaluate': 0.29, 'data_cos': 0.4214359631185481, 'challenger_cos': 0.5235674540397135, 'sign_test_result': 'The difference is statistically significant.\nChallenger model is better.\n'},

    {'name': 'Forza Horizon 4', 'our_idf_evaluate': 0.18, 'bot_idf_evaluate': 0.27, 'data_cos': 0.3982851445144679, 'challenger_cos': 0.4688844085185497, 'sign_test_result': 'The difference is statistically significant.\nChallenger model is better.\n'},

    {'name': 'The Witcher 3: Wild Hunt', 'our_idf_evaluate': 0.06, 'bot_idf_evaluate': 0.15, 'data_cos': 0.4017122151398771, 'challenger_cos': 0.40938839515832043, 'sign_test_result': 'The difference is statistically significant.\nChallenger model is better.\n'},

    {'name': 'Cyberpunk 2077', 'our_idf_evaluate': 0.23, 'bot_idf_evaluate': 0.28, 'data_cos': 0.4656272613108446, 'challenger_cos': 0.4409893951195657, 'sign_test_result': 'The difference is not statistically significant.\n'},

    {'name': 'ELDEN RING', 'our_idf_evaluate': 0.13, 'bot_idf_evaluate': 0.26, 'data_cos': 0.3884870071411667, 'challenger_cos': 0.4659410507678186, 'sign_test_result': 'The difference is statistically significant.\nChallenger model is better.\n'},

    {'name': 'Destiny 2', 'our_idf_evaluate': 0.07, 'bot_idf_evaluate': 0.3, 'data_cos': 0.38014683304759583, 'challenger_cos': 0.5714057173413745, 'sign_test_result': 'The difference is statistically significant.\nChallenger model is better.\n'},

    {'name': 'Nine Sols', 'our_idf_evaluate': 0.21, 'bot_idf_evaluate': 0.33, 'data_cos': 0.3753836231963108, 'challenger_cos': 0.5461593710986591, 'sign_test_result': 'The difference is statistically significant.\nChallenger model is better.\n'},

    {'name': 'Counter-Strike 2', 'our_idf_evaluate': 0.18, 'bot_idf_evaluate': 0.13, 'data_cos': 0.43020976297590763, 'challenger_cos': 0.37808339723454143, 'sign_test_result': 'The difference is statistically significant.\nOur model is better.\n'},

    {'name': 'World of Tanks', 'our_idf_evaluate': 0.17, 'bot_idf_evaluate': 0.16, 'data_cos': 0.39546496434478395, 'challenger_cos': 0.40738556713103224, 'sign_test_result': 'The difference is not statistically significant.\n'},

    {'name': 'NARAKA: BLADEPOINT', 'our_idf_evaluate': 0.12, 'bot_idf_evaluate': 0.21, 'data_cos': 0.3360994132688929, 'challenger_cos': 0.35395976083022945, 'sign_test_result': 'The difference is statistically significant.\nChallenger model is better.\n'},

    {'name': 'PUBG: BATTLEGROUNDS', 'our_idf_evaluate': 0.16, 'bot_idf_evaluate': 0.27, 'data_cos': 0.374485925029323, 'challenger_cos': 0.4895320053266977, 'sign_test_result': 'The difference is statistically significant.\nChallenger model is better.\n'},

    {'name': 'Left 4 Dead 2', 'our_idf_evaluate': 0.12, 'bot_idf_evaluate': 0.3, 'data_cos': 0.3433058964751931, 'challenger_cos': 0.5655412171826097, 'sign_test_result': 'The difference is statistically significant.\nChallenger model is better.\n'},

    {'name': 'Among Us', 'our_idf_evaluate': 0.22, 'bot_idf_evaluate': 0.23, 'data_cos': 0.4884146349921813, 'challenger_cos': 0.5046393873639301, 'sign_test_result': 'The difference is not statistically significant.\n'},

    {'name': "Tom Clancy's Rainbow Six Siege", 'our_idf_evaluate': 0.12, 'bot_idf_evaluate': 0.32, 'data_cos': 0.3335750244235953, 'challenger_cos': 0.4159414409425402, 'sign_test_result': 'The difference is statistically significant.\nChallenger model is better.\n'},

    {'name': 'DayZ', 'our_idf_evaluate': 0.15, 'bot_idf_evaluate': 0.19, 'data_cos': 0.32780911285020553, 'challenger_cos': 0.375017634756443, 'sign_test_result': 'The difference is statistically significant.\nChallenger model is better.\n'},

    {'name': 'FIFA 22', 'our_idf_evaluate': 0.16, 'bot_idf_evaluate': 0.27, 'data_cos': 0.35588246975198035, 'challenger_cos': 0.5523817472945519, 'sign_test_result': 'The difference is statistically significant.\nChallenger model is better.\n'},

    {'name': 'NBA 2K24', 'our_idf_evaluate': 0.1, 'bot_idf_evaluate': 0.23, 'data_cos': 0.29115453605160013, 'challenger_cos': 0.45320276461866377, 'sign_test_result': 'The difference is statistically significant.\nChallenger model is better.\n'},

    {'name': 'DEAD OR ALIVE Xtreme Venus Vacation', 'our_idf_evaluate': 0.12, 'bot_idf_evaluate': 0.15, 'data_cos': 0.38887542017068366, 'challenger_cos': 0.49963801394071183, 'sign_test_result': 'The difference is statistically significant.\nChallenger model is better.\n'},

    {'name': 'Albion Online', 'our_idf_evaluate': 0.16, 'bot_idf_evaluate': 0.22, 'data_cos': 0.4028982844694964, 'challenger_cos': 0.41936925454323387, 'sign_test_result': 'The difference is statistically significant.\nChallenger model is better.\n'},

    {'name': 'Dead by Daylight', 'our_idf_evaluate': 0.4, 'bot_idf_evaluate': 0.18, 'data_cos': 0.6709965645266425, 'challenger_cos': 0.4004778914568428, 'sign_test_result': 'The difference is statistically significant.\nOur model is better.\n'},

    {'name': 'Palworld', 'our_idf_evaluate': 0.11, 'bot_idf_evaluate': 0.23, 'data_cos': 0.2943021439502852, 'challenger_cos': 0.4576412358152127, 'sign_test_result': 'The difference is statistically significant.\nChallenger model is better.\n'},

    {'name': 'Cities: Skylines II', 'our_idf_evaluate': 0.19, 'bot_idf_evaluate': 0.17, 'data_cos': 0.48913200282922076, 'challenger_cos': 0.4203151839163236, 'sign_test_result': 'The difference is not statistically significant.\n'},

    {'name': 'Hades II', 'our_idf_evaluate': 0.1, 'bot_idf_evaluate': 0.29, 'data_cos': 0.34020738723837934, 'challenger_cos': 0.5617160883891694, 'sign_test_result': 'The difference is statistically significant.\nChallenger model is better.\n'},

    {'name': 'Yu-Gi-Oh!  Master Duel', 'our_idf_evaluate': 0.12, 'bot_idf_evaluate': 0.17, 'data_cos': 0.3467899898348305, 'challenger_cos': 0.4819787202136279, 'sign_test_result': 'The difference is statistically significant.\nChallenger model is better.\n'},

    {'name': 'Fall Guys', 'our_idf_evaluate': 0.13, 'bot_idf_evaluate': 0.23, 'data_cos': 0.33990475360841116, 'challenger_cos': 0.45163505004505644, 'sign_test_result': 'The difference is statistically significant.\nChallenger model is better.\n'},

    {'name': 'Geometry Dash', 'our_idf_evaluate': 0.12, 'bot_idf_evaluate': 0.14, 'data_cos': 0.4661270435232539, 'challenger_cos': 0.3287852195519319, 'sign_test_result': 'The difference is not statistically significant.\n'},

    {'name': 'Resident Evil Village', 'our_idf_evaluate': 0.17, 'bot_idf_evaluate': 0.21, 'data_cos': 0.4550752175756437, 'challenger_cos': 0.5328048972826693, 'sign_test_result': 'The difference is statistically significant.\nChallenger model is better.\n'},

    {'name': 'Raft', 'our_idf_evaluate': 0.23, 'bot_idf_evaluate': 0.23, 'data_cos': 0.4612639474891009, 'challenger_cos': 0.5096494802034884, 'sign_test_result': 'The difference is statistically significant.\nChallenger model is better.\n'},

    {'name': 'GUILTY GEAR -STRIVE-', 'our_idf_evaluate': 0.21, 'bot_idf_evaluate': 0.26, 'data_cos': 0.416763432845066, 'challenger_cos': 0.5077714992584853, 'sign_test_result': 'The difference is statistically significant.\nChallenger model is better.\n'},

    {'name': 'Warframe', 'our_idf_evaluate': 0.41, 'bot_idf_evaluate': 0.42, 'data_cos': 0.6253606676041447, 'challenger_cos': 0.6626651384906851, 'sign_test_result': 'The difference is statistically significant.\nChallenger model is better.\n'},

    {'name': "Baldur's Gate 3", 'our_idf_evaluate': 0.13, 'bot_idf_evaluate': 0.22, 'data_cos': 0.3688723926866534, 'challenger_cos': 0.45392024325275643, 'sign_test_result': 'The difference is statistically significant.\nChallenger model is better.\n'},

    {'name': 'Apex Legends', 'our_idf_evaluate': 0.14, 'bot_idf_evaluate': 0.14, 'data_cos': 0.4327544075934476, 'challenger_cos': 0.39988565537126597, 'sign_test_result': 'The difference is not statistically significant.\n'},

    {'name': 'Stardew Valley', 'our_idf_evaluate': 0.2, 'bot_idf_evaluate': 0.28, 'data_cos': 0.3866960952889325, 'challenger_cos': 0.47667706785506037, 'sign_test_result': 'The difference is statistically significant.\nChallenger model is better.\n'},

    {'name': "Assassin's Creed Valhalla", 'our_idf_evaluate': 0.13, 'bot_idf_evaluate': 0.19, 'data_cos': 0.37146556747299014, 'challenger_cos': 0.5099164626940006, 'sign_test_result': 'The difference is statistically significant.\nChallenger model is better.\n'},

    {'name': 'Hogwarts Legacy', 'our_idf_evaluate': 0.22, 'bot_idf_evaluate': 0.39, 'data_cos': 0.46888011536588936, 'challenger_cos': 0.625330862274383, 'sign_test_result': 'The difference is statistically significant.\nChallenger model is better.\n'},

    {'name': "Tom Clancy's The Division 2", 'our_idf_evaluate': 0.23, 'bot_idf_evaluate': 0.35, 'data_cos': 0.42697369443819067, 'challenger_cos': 0.5190614150470766, 'sign_test_result': 'The difference is statistically significant.\nChallenger model is better.\n'},

    {'name': 'Halo Infinite', 'our_idf_evaluate': 0.04, 'bot_idf_evaluate': 0.12, 'data_cos': 0.34302618410722796, 'challenger_cos': 0.3564800743430096, 'sign_test_result': 'The difference is not statistically significant.\n'},

    {'name': 'Detroit: Become Human', 'our_idf_evaluate': 0.23, 'bot_idf_evaluate': 0.29, 'data_cos': 0.4214359631185481, 'challenger_cos': 0.5235674540397135, 'sign_test_result': 'The difference is statistically significant.\nChallenger model is better.\n'},
]


#analy = Analysis()
# analy.plot_score(score_list)
# analy.table_perf(cpu_time_list)
# analy.plot_cl_score(cl_list)
# analy.table_clscore(cl_list)
# analy.table_perf(gpu_time_list)
# analy.printgames(games)