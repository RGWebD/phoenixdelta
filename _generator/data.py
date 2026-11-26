# Phoenix Delta LLC — single source of facts. Sources: client logo card + services list screenshot from Reese (Nov 25 2026).
NAME="Phoenix Delta LLC"; SHORT="Phoenix Delta"; TAGLINE="Installation and Repair"
REPO="phoenixdelta"; BASE=f"https://rgwebd.github.io/{REPO}/"
PHONE="904-562-9356"; PHONE_FMT="(904) 562-9356"; TEL="tel:+19045629356"; SMS="sms:+19045629356"
EMAIL=""   # none yet: when the client has one, set it here and the form adds an email button
AREA="Jacksonville, FL and surrounding areas"
COUNTIES=["Duval","Clay","St. Johns","Nassau"]
# service groups -> services (every trade from the client's list, nothing added)
GROUPS=[
 dict(id="interior",t="Interior finishes",ic="paint",k="Paint, plaster & seal",
      s="Fresh walls, smooth surfaces and tight seams inside the house.",
      items=[("paint","Painting","Painting for your home, from one room to the whole house."),("plaster","Plastering","Plaster installation and repair for walls and ceilings."),("caulk","Caulking","Caulking and re-caulking to seal joints and seams.")]),
 dict(id="remodel",t="Interior remodeling",ic="remodel",k="Non-licensed scope",
      s="Interior updates that don’t call for a state-licensed trade.",
      items=[("remodel","Interior remodeling","Interior remodeling projects that don’t include work requiring a state license."),("cabinet","Cabinetry","Cabinet installation and repair."),("handy","Handyman services","The repair list, the punch list and the odd jobs.")]),
 dict(id="floors-stone",t="Floors, tile & stone",ic="stone",k="Underfoot & on the counter",
      s="Flooring, plus decorative stone, tile, marble, granite and terrazzo.",
      items=[("floor","Flooring","Flooring installation and repair."),("stone","Decorative stone & tile","Decorative stone, tile, marble, granite and terrazzo installation.")]),
 dict(id="exterior",t="Exterior surfaces",ic="stucco",k="Stucco & pressure washing",
      s="Outside walls and surfaces, refreshed and refinished.",
      items=[("stucco","Stuccoing","Stucco application and repair."),("washer","Pressure washing","Pressure washing for the outside of your home and property.")]),
 dict(id="driveways-courts",t="Driveways & courts",ic="drive",k="Paved & playable",
      s="Driveway and tennis court installation.",
      items=[("drive","Driveway installation","New driveway installation."),("court","Tennis court installation","Tennis court installation.")]),
 dict(id="awnings-iron",t="Awnings & ornamental iron",ic="awning",k="Shade & style",
      s="Canvas awning and ornamental iron installation.",
      items=[("awning","Canvas awnings","Canvas awning installation."),("iron","Ornamental iron","Ornamental iron installation.")]),
]
ALL=[(i,t,d,g["id"]) for g in GROUPS for (i,t,d) in g["items"]]
FAQ=[
 ("What does Phoenix Delta do?","Home installation and repair across many trades: painting, plastering, caulking, interior remodeling (non-licensed work), cabinetry, handyman services, flooring, decorative stone, tile, marble, granite and terrazzo, stuccoing, pressure washing, driveway and tennis court installation, and canvas awning and ornamental iron installation."),
 ("Where do you work?","Jacksonville, Florida and the surrounding areas, including Duval, Clay, St. Johns and Nassau counties. Not sure if you’re in range? Call and ask."),
 ("How do I get an estimate?",f"Call {PHONE}, or fill in the estimate form on the Contact page. It opens a pre-filled text message to {PHONE} on your phone, so nothing is sent until you press send."),
 ("Can you handle more than one job on the same visit?","That’s the idea behind Phoenix Delta: one call for many jobs. Tell us everything on your list when you call and we’ll talk it through."),
 ("Do you do electrical, plumbing or structural work?","Interior remodeling here covers non-licensed work only. Work that requires a state-licensed trade isn’t part of the service list."),
]
# Photo slots. To swap in a real photo: drop  assets/img/<name>-1600.webp + <name>-800.webp  into sitegen/assets/img,
# then set the slot's third value to "<name>" and rebuild. Alt text = the label.
SLOTS={
 "home":[("s-paint","Painting",None),("s-floor","Flooring & tile",None),("s-exterior","Pressure washing & stucco",None)],
 "about":[("a1","Interior finishes",None),("a2","Cabinetry",None),("a3","Decorative stone & tile",None),("a4","Driveways & courts",None),("a5","Awnings & ornamental iron",None),("a6","Handyman jobs",None)],
 "interior":[("g-interior","Painting & plastering",None)],"remodel":[("g-remodel","Interior remodeling & cabinetry",None)],
 "floors-stone":[("g-floors","Floors, tile & stone",None)],"exterior":[("g-exterior","Stucco & pressure washing",None)],
 "driveways-courts":[("g-drive","Driveways & courts",None)],"awnings-iron":[("g-awning","Awnings & ornamental iron",None)],
}
