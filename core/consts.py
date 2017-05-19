from cmd2 import Cmd
logo1 = """                                     .-:/+osyhhddmmmNNNNNmmmddhyso+:            
                             .:+sydNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMy            
                        ./sdNMMMMMMMMMMMMMNmddhyyysssyyyhhdNMMMMMMM+            
                    .+yNMMMMMMMMMmhs+/-.`                   `-/sdMM.            
                 :smMMMMMMNds+:.                     `hyso/-`    `-             
              -sNMMMMMds/.                           `MMMMMMMNds/`              
           .omMMMMms:`                               `MMMMMMMMMMMMdo.           
         -yMMMMd+.                                    -:/osydNMMMMMMMd/         
       -hMMMNs.                      sdhs                     `:ohNMMMMm/       
     `sMMMm+`                        dMMh            yMN:/dd+      :yMMMMd.     
    .mMMNo`                          dMMo     .smNmh.yMMdso/         `oNMMN/    
   :NMMd. ---`                       dMM/ :/`.NMd`hM/sMMs              .hMMM/   
  -NMMs   NMMh                 -/:`  dMM:hMy.oMMydd+ oMM-                sMMN.  
 `mMM+    mMMs        --     :mMmNM+ hMMMm:  yMM:`-+.+MM.                 sMMy  
 +MMs     dMM/      .hMMMd: :MMh`oMy yMM+hMm./MMsdMm:-sy`                 `NMN` 
 mMN`     dMM--yy+``mMh.dMm mMm   `  yMN `mMy -oys:       +Nm+             sMM- 
`MMs      dMMyNNMMs`/+/+mMM NMy .sMd`sMm  oMN.    .-      oMMo  `+hhy+     +MM: 
-MM/      dMM+ :MMh`yMmydMM`.yNdMm+`  ``         .mMh     oMM/ .mMm/NMo    oMM. 
:MM:      dMN   NMm.NmoodMM.   ..            :o. ``.   +dNMMM/`mMm:hMN:    mMm  
-MMs      hMd   hMN .oys+yh.`-`            +NMMy hMM. yMM/oMM//MMmds//.   +MM/  
 NMN.     :s+   :yy         yMh`ymd:.ss+``mMMd+. sMM`:MM+ sMM--MM/ +NMs  +MMs   
 :MMm`                     `/+/ yMMhdmMM/`hMN:   sMM`yMM`.dMM- -smNNs. `sMMs    
  /MMN:                    .MMN yMMd`:MMs  .oNNo +MM`+MMmNoMM-       `+NMN:     
   -mMMh.                  `MMm sMM: `NMm   .mMM.:MM  -oo. ym:     .sNMNo`      
    `sMMMh:                 MMh oMM-  yMM-`sMMN:  --            .+dMMNo`        
      .sNMMms-              MMy /NM.  :MMs.yh+`             `:smMMMd/`          
        `+mMMMNho-`         dMy        -/:              -+smMMMMmo.             
           -odMMMMMmyo:.                           .-/ohmMMMMMMdo-                
              `/smMMMMMMMNdhso+/:::--:://+osyhdNMMMMMMMMNds:`                   
                  `-+sdNMMMMMMMMMMMMMMMMMMMMMMMMMNmhs+:.                        
                        `-:/+osyyhhhdhhhyyso+/:.`                               
"""
logo2="""
                                                                          DUDE...                                    
"""
example_usage = """
Most typical use of HID:
 1.  list_modules - to see available module.
 2.  info module <choosen module> - to see information about modules.
 3.  use module <choosen module> - to activate module.
 4.  info parameter <parameter_name> - to see information about module parameter. 
 5.  set parameter <parameter_name> <parameter value> - to set value for module parameter. 
 6.  list_devices - to see device supporting seleced module.
 7.  info device <device_name> - to see information about device.
 8.  use device <device> - to select device.
 9.  info parameter <parameter_name> <parameter value> - to see information about device parameter. 
 10. set parameter <parameter_name> <parameter value> - to set value for device parameter. 
 11. list_payload - to see payload for choosen module.
 12. info payload <payload_name> - to see informatin about payload.
 13. info action <action name> - optional - to see used actions description.
 14. use payload <payload> - to set payload.
 15. info parameter <parameter_name> <parameter value> - to see information about payload parameter. 
 16. set parameter <parameter_name> <parameter value> - to set value for payload parameter. 
 17. show -l - to verify all parameters values
 18. execute - to program device.

Type: help <command> for more information about specific command.
            """
modules_dir = "modules"
payloads_dir = "payloads"
devices_dir = "devices"
actions_dir = "actions"
core_dir = "core"
