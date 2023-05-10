# create scrollable frame
self.scrollable_frame = customtkinter.CTkScrollableFrame(
     self.main_frame, label_text="CTkScrollableFrame")
 self.scrollable_frame.pack(side="left", fill="both", expand=True)

  self.scrollable_frame_switches = []
   for i in range(5):
        switch = customtkinter.CTkSwitch(
            master=self.scrollable_frame, text=f"CTkSwitch {i}")
        switch.grid(row=i, column=0, padx=10, pady=(0, 20))
        self.scrollable_frame_switches.append(switch)

    # set default values
    self.scrollable_frame_switches[0].select()
    self.scrollable_frame_switches[4].select()
