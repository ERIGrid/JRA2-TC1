#Put local path where you want to create yur new python file1
file1= open(r"C:\Users\LocalAdmin\Desktop\WG-TC1\Upscaledfin\IOlist.txt",'w')

#writing
for i in range(1,33):
    file1.write("ElmGenstat.WT_%i.m:Psum:bus1\n"%(i))
    file1.write("ElmGenstat.WT_%i.m:u1:bus1\n"%(i))
    file1.write("ElmGenstat.WT_%i.m:phiu1:bus1\n"%(i))
    file1.write("ElmGenstat.WT_%i.s:id\n"%(i))
    file1.write("ElmGenstat.WT_%i.s:iq\n"%(i))
    file1.write("ElmGenstat.WT_%i.e:Pnom\n"%(i))
    file1.write("ElmGenstat.WT_%i.m:P:bus1\n"%(i))
    file1.write("ElmGenstat.WT_%i.m:Q:bus1\n"%(i))

#writing generators
file1.write("ElmSym.G1.s:xspeed\n")
file1.write("ElmSym.G1.s:xphi\n")
file1.write("ElmSym.G2.s:xspeed\n")
file1.write("ElmSym.G2.s:xphi\n")


#writing outputs
for i in range(1,33):
    file1.write("EvtParam.WTframe_%i.iq_ref_in\n"%(i))
    file1.write("EvtParam.WTframe_%i.id_ref_in\n"%(i))

#Events
file1.write("EvtParam.event.trigger\n")
file1.write("EvtParam.event.event_string\n")

file1.close()

