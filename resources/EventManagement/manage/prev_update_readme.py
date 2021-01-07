def update_readme(self):
    """Add (update) table row as per meta.
    old version
    """
    bkp = DIR_DATA.joinpath('backup', self.readme.name)
    # Backup the file
    shutil.copy(self.readme, bkp)

    # Get the text
    try:
        readme_txt = get_file_lines(self.readme)
    except FileNotFoundError:
        # try reverting to previously backup copy
        shutil.copy(bkp, self.readme)
        readme_txt = get_file_lines(self.readme)

    # Get the table data:
    i, j = self.tbl_delims
    off1 = 3  # offset 1 = delim row + 2 header rows
    off2 = -1 if self.empty_lastrow else 0
    tbl = readme_txt[i+off1:j+off2]

    #| #| Speaker| Talk Transcript| Transcriber| Status| Notes|
    # Construct last row:
    pipestr = '| '
    # Talk Transcript = md link: [title](year/readme)
    talk = F"[{self.event_dict['title']}]"
    talk += F"({self.event_dict['year']}/{self.event_dict['transcript_md']})"
    fields = [self.event_dict['idn'],
              self.event_dict['presenter'],
              talk, 
              self.event_dict['transcriber'],
              self.event_dict['status'],
              self.event_dict['notes']
             ]
    ro = pipestr + pipestr.join(fields) + pipestr + '\n'
    tbl.append(ro)

    # Update main text w/table data:
    readme_txt[i+off1:j] = tbl

    # Re-create readme:
    with open(self.readme, 'w') as fh:
        fh.writelines(readme_txt)

    # Refresh info:
    self.refresh_tbl_info()
    #F'Table in {self.readme.name} was updated.'
    return