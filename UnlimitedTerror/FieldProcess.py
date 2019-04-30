# coding=utf-8
"""
该文件包含了一些用于将字段处理为字符串或将字符串处理回字段的函数
需要注意的是所有的输入输出均为str类型或者包含str的list
"""
import re  # 调取正则表达式

TxtSign = '▓'  # 标示符
test = '姓名：Max\n性别：Male\n年龄：18\n种族/国籍：China\n身高体重：180cm\n语言：Chinese\n美德/恶德：A\n外貌：a\n概述：123\n1：1234\n12：12345\n123：123456\n' \
       '▓▓▓屬性：\n▓力量=内在(1)+完美(1)=2 传奇（0)\n▓敏捷=内在(1)+完美(1)=2 传奇（0)\n▓耐力=内在(1)+完美(1)=2 传奇（0)\n' \
       '▓智力=内在(1)+完美(1)=2 传奇（0)\n▓感知=内在(1)+完美(1)=2 传奇（0)\n▓决心=内在(1)+完美(1)=2 传奇（0)\n' \
       '▓风度=内在(1)+完美(1)=2 传奇（0)\n▓操控=内在(1)+完美(1)=2 传奇（0)\n▓沉着=内在(1)+完美(1)=2 传奇（0)\n' \
       '▓▓▓技能：\n▓射击：1 专业：手枪\n' \
       '▓▓▓衍生属性：\n▓体积=标准（5）=5\n▓生命值=耐力（2）+体积（5）=7\n'  # 这是一个测试用字符串


# 向字符串中添加基础信息
def AddPersonalInfo(
        Log,
        Name,
        Gender,
        Age,
        Race,
        Body,
        Language,
        Morality,
        Apperance,
        Background):
    Log += '姓名：' + Name + '\n' + \
           '性别：' + Gender + '\n' + \
           '年龄：' + Age + '\n' + \
           '种族/国籍：' + Race + '\n' + \
           '身高体重：' + Body + '\n' + \
           '语言：' + Language + '\n' + \
           '美德/恶德：' + Morality + '\n' + \
           '外貌：' + Apperance + '\n' + \
           '概述：' + Background + '\n'
    return Log


# 向字符串中添加一行专长项


def AddSpeciality(Log, TheNameOfSpeciality, TheMessageOfSpeciality):
    Log += TheNameOfSpeciality + '：' + TheMessageOfSpeciality + '\n'
    return Log


# 向字符串中添加所有的属性相关信息
# TypeOfAttributes 保存属性的类型
# Attribute 为9个一维数组构成的二维数组，其中的每个属性应为字符


def AddAttributes(Log, TypeOfAttributes, Attributes):
    AT = ['力量', '敏捷', '耐力', '智力', '感知', '决心', '风度', '操控', '沉着']
    Log += TxtSign * 3 + '屬性：' + '\n'
    for item in range(0, len(Attributes)):
        Log += TxtSign + AT[item] + '='
        SumAttributes = int(0)
        for TypeNum in range(0, len(TypeOfAttributes)):
            Log += TypeOfAttributes[TypeNum] + \
                   '(' + Attributes[item][TypeNum] + ')+'
            SumAttributes += int(Attributes[item][TypeNum])
        Log = Log[:-1] + '=' + str(SumAttributes) + ' 传奇（' + \
              str(int((SumAttributes - 1) / 5)) + ')\n'
    return Log


# 向字符串中添加所有的技能
# SkillList 为 若干个3个属性的一维数组构成的二维数组
# 一维数组第一个属性为技能名，第二个为技能等级，第三个为专业


def AddSkill(Log, SkillList):
    Log += TxtSign * 3 + '技能：' + '\n'
    for Skill in SkillList:
        Log += TxtSign + Skill[0] + '：' + Skill[1] + ' 专业：' + Skill[2] + '\n'
    return Log


# 向字符串中添加所有衍生属性
# DerivedAttributesList为 若干个3个属性的一维数组构成的二维数组
# 一维数组第一个属性为属性名，第二个为属性内容，第三个为总和


def AddDerivedAttributes(Log, DerivedAttributesList):
    Log += TxtSign * 3 + '衍生属性：' + '\n'
    for DerivedAttributes in DerivedAttributesList:
        Log += TxtSign + DerivedAttributes[0] + '=' + \
               DerivedAttributes[1] + '=' + DerivedAttributesList[2] + '\n'
    return Log


# 从字符串中读取个人信息


def ReadPersonalInfo(Log):
    PersonalInfo = []
    PointList = ['姓名', '性别', '年龄', '种族/国籍', '身高体重', '语言', '美德/恶德', '外貌', '概述']
    for item in PointList:
        Temp = re.findall(r'' + item + '：(.*)\n', Log)
        PersonalInfo += Temp
    return PersonalInfo


# 从字符串中读取专长项


def ReadSpeciality(Log):
    Speciality = re.findall(r'概述：.*\n([\s\S]*)▓▓▓屬性：\n', Log)
    ListSpecialityName = re.findall(r'(.*)：.*\n', Speciality[0])
    ListSpecialityInfo = re.findall(r'.*：(.*)\n', Speciality[0])
    ListSpeciality = [ListSpecialityName, ListSpecialityInfo]
    return ListSpeciality


# 从字符串中读取属性,最后一位位一维数组保存属性加值类型


def ReadAttributes(Log):
    AT = ['力量', '敏捷', '耐力', '智力', '感知', '决心', '风度', '操控', '沉着']
    Attributes = re.findall(r'▓▓▓屬性：\n([\s\S]*)▓▓▓', Log)
    Attributes = Attributes[0]
    ListAttributes = []
    for EachAT in AT:
        # 读取每一行属性
        Temp = re.findall(r'' + TxtSign + EachAT + '=(.*)=.*\n', Attributes)
        ListAttributes += Temp

    Attributes = ListAttributes
    ListAttributes = []
    # 读取属性加值类型
    TypeOfAttributes = re.findall(r'\+?(.*?)\(\d*\)', Attributes[0])
    # 从每一行属性中按加值类型读取点数
    for item in Attributes:
        EachNum = []
        for EachType in TypeOfAttributes:
            Num = re.findall(r'' + EachType + r'\((\d*)\)', item)
            EachNum += Num
        ListAttributes.append(EachNum)
    ListAttributes.append(TypeOfAttributes)
    return ListAttributes


# 读取技能相关信息


def ReadSkill(Log):
    SkillTEXT = re.findall(r'▓▓▓技能：\n([\s\S]*)▓▓▓', Log)
    SkillTEXT = SkillTEXT[0]
    TypeOfSkill = re.findall(r'▓(.*)：.* 专业：.*\n', SkillTEXT)
    Skill = []
    # 读取每一行数据生成一维数组添加到Skill中
    for item in TypeOfSkill:
        SkillLine = [item]
        SkillLevel = re.findall(r'▓' + item + '：(.*) 专业：.*\n', SkillTEXT)
        SkillMajor = re.findall(r'▓' + item + '：.* 专业：(.*)\n', SkillTEXT)
        SkillLine += SkillLevel
        SkillLine += SkillMajor
        Skill.append(SkillLine)
    return Skill


# 读取衍生属性相关信息


def ReadDerivedAttributes(Log):
    DerivedAttributesText = re.findall(r'▓▓▓衍生属性：\n([\s\S]*)', Log)
    DerivedAttributesText = DerivedAttributesText[0]
    DerivedAttributesName = re.findall(r'▓(.*)=.*=.*\n', DerivedAttributesText)
    DerivedAttributesList = []
    # 读取每一行属性生成一维数组添加到DERivedAttributesList中
    for item in DerivedAttributesName:
        Line = [item]
        DerivedAttributesContent = re.findall(
            r'▓' + item + '=(.*)=.*\n', DerivedAttributesText)
        Line += DerivedAttributesContent
        DerivedAttributesResult = re.findall(
            r'▓' + item + '=.*=(.*)\n', DerivedAttributesText)
        Line += DerivedAttributesResult
        DerivedAttributesList.append(Line)
    return DerivedAttributesList
