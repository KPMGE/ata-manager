from googleapiclient.errors import HttpError

class Spreadsheet:

  def __init__(self, service, spreadsheet_id, range):
    self.service = service
    self.range = range
    self.spreadsheetId = spreadsheet_id
    self.content = self.__get_content(spreadsheet_id, range)

  def __get_content(self, spreadsheet_id, range):
    
    try:
      content = self.service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range).execute()
      values = content.get('values', [])
      # print(values)

    except HttpError as error:
      print(error)

    return values  


  def __update_status(self, index):
    
    range = f"B{index+2}:B{index+3}"
    value = [[1]]

    try:
      self.service.spreadsheets().values().update(spreadsheetId=self.spreadsheetId, 
      range=range, valueInputOption="USER_ENTERED", body={'values': value}).execute()
      print('Status updated sucefully!')
    except HttpError as error:
      print(error)

  def __reset_status(self): 
    array = [[0]]*13
    try:
      self.service.spreadsheets().values().update(spreadsheetId=self.spreadsheetId, 
      range="!B2:B14", valueInputOption="USER_ENTERED", body={'values': array}).execute()
      print('Status reseted sucefully!')
    except HttpError as error:
      print(error)


  #Retorna todos os emails
  def get_students(self):
    students = []
    for person in self.content:
      students.append({'name': person[0],'email':person[2]})
    # print(emails)
    students.pop(0)
    return students


  #Retorna o horário da reunião
  def get_time(self):
    return self.content[1][4]


  def get_todays_writer(self):
    matrix = self.content
    matrix.pop(0)

    for i,person in enumerate(matrix):

      #Caso a pessoa não esteja presente, pula para o próximo
      if not int(person[3]):
        continue

      #Caso a pessoa não tenha preenchido a ata ainda
      if not int(person[1]):
        name = person[0]
        self.__update_status(i)
        return name

    self.__reset_status()

    # Deve-se atualizar o conteúdo pra recursão funcionar
    self.content = self.__get_content(self.spreadsheetId, self.range)
    return self.get_todays_writer()
