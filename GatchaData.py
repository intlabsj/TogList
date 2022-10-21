from WebRequest import run_all
import base64
import pandas as pd
import numpy as np

class GatchaData:
    def __init__(self, ID):
        self.ID = ID
        self.encoded_ID = base64.b64encode(ID.encode('ascii'))
        self.url = "https://tog.ngelgames.com/history/" + self.encoded_ID.decode()
        self.class_cnt, self.ts_cnt = dict(), dict()

        self.entropy = {"엔트로피": [0] * 6}

        self.cls_list = {
            "legend_character": "전설캐릭",
            "legend_weapon": "전설무기",
            "hero_character": "영웅캐릭",
            "hero_weapon": "영웅무기",
            "rare_weapon": "희귀무기",
            "advanced_weapon": "고급무기"}

        self.data = dict()
        for file in self.cls_list.keys():
            self.class_cnt[file] = 0

            fp = open("./list/" + file + ".txt", "r", encoding="UTF-8")
            while True:
                line = fp.readline().strip('\n')
                if line == '': break
                self.data[line] = {"class": file, "count": 0}

            fp.close()

        self.trigger = self.get_gatcha_list()

    def get_gatcha_list(self):
        self.gatcha_list = run_all(self.url)
        if self.gatcha_list == False or self.gatcha_list == -1:
            return self.gatcha_list

        for gl in self.gatcha_list:
            name, _, _ = gl.values()
            self.add_itemcnt(name)

        self.add_entropy()
        return True

    def get_entropy(self):
        temp_dict = {}

        for key, value in self.data.items():
            if key == '백천경 쿤' or key == '연이화': continue
            if value["class"] not in temp_dict:
                temp_dict[value["class"]] = list()
            temp_dict[value["class"]].append(value["count"])

        df_dict = {"엔트로피": []}
        for key, value_arr in temp_dict.items():
            value = np.asarray(value_arr)
            normalize = np.zeros(value.shape) if np.sum(value) == 0.0 else value/np.sum(value)
            normalize[np.where(normalize == 0.0)] = 1e-8

            entropy = sum(-normalize * (np.log(normalize) / np.log(len(normalize))))

            df_dict["엔트로피"].append(entropy)

        return df_dict

    def add_entropy(self):
        entropy = self.get_entropy()

        self.entropy["엔트로피"] = [self.entropy["엔트로피"][idx] + entropy["엔트로피"][idx] for idx in range(6)]

    def add_itemcnt(self, item):
        self.data[item]["count"] += 1
        self.class_cnt[self.data[item]["class"]] += 1

    def get_itemcnt(self, item):
        return self.data[item]["count"]

    def get_clscnt(self, cls):
        return self.class_cnt[cls]

    def print_from_gatcha(self):
        df_dict = {"아이템 이름": [], "등장 횟수": [], "등장 확률": []}
        total = sum(list(self.class_cnt.values()))
        index = list()
        for key, value in self.data.items():
            df_dict["아이템 이름"].append(key)
            df_dict["등장 횟수"].append(value["count"])
            percent = "{0:.2f}%".format((value["count"] / total) * 100)
            df_dict["등장 확률"].append(percent)
            index.append(self.cls_list[value["class"]])

        return pd.DataFrame(df_dict, columns=df_dict.keys(), index=index)

    def print_entropy(self):
        return pd.DataFrame(self.entropy, columns=self.entropy.keys(), index=self.cls_list.values())
