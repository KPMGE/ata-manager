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
  def get_emails(self):
    emails = []
    for person in self.content:
      emails.append(person[2])
    # print(emails)
    return emails


  #Retorna o horário da reunião
  def get_time(self):
    # print(self.content[1][4])
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
        email = person[2]
        self.__update_status(i)
        return name, email

    self.__reset_status()

    # Deve-se atualizar o conteúdo pra recursão funcionar
    self.content = self.__get_content(self.spreadsheetId, self.range)
    return self.get_todays_writer()
