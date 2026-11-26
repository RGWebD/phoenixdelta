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
 dict(id="remodel",t="Remodeling & handyman",ic="remodel",k="Updates & odd jobs",
      s="Interior updates, repairs and the punch list.",
      items=[("remodel","Interior remodeling","Interior remodeling projects for your home."),("handy","Handyman services","The repair list, the punch list and the odd jobs.")]),
 dict(id="floors-stone",t="Floors, tile & stone",ic="stone",k="Underfoot & all around",
      s="Flooring, plus decorative stone and tile.",
      items=[("floor","Flooring","Flooring installation and repair."),("stone","Decorative stone & tile","Decorative stone and tile installation.")]),
 dict(id="exterior",t="Exterior & outdoor",ic="washer",k="Wash, shade & iron",
      s="Outside surfaces cleaned up, plus canvas awnings and ornamental iron.",
      items=[("washer","Pressure washing","Pressure washing for the outside of your home and property."),("awning","Canvas awnings","Canvas awning installation."),("iron","Ornamental iron","Ornamental iron installation.")]),
]
ALL=[(i,t,d,g["id"]) for g in GROUPS for (i,t,d) in g["items"]]
FAQ=[
 ("What does Phoenix Delta do?","Home installation and repair across many trades: painting, plastering, caulking, interior remodeling, handyman services, flooring, decorative stone and tile, pressure washing, and canvas awning and ornamental iron installation."),
 ("Where do you work?","Jacksonville, Florida and the surrounding areas, including Duval, Clay, St. Johns and Nassau counties. Not sure if you’re in range? Call and ask."),
 ("How do I get an estimate?",f"Call {PHONE}, or fill in the estimate form on the Contact page. It opens a pre-filled text message to {PHONE} on your phone, so nothing is sent until you press send."),
 ("Can you handle more than one job on the same visit?","That’s the idea behind Phoenix Delta: one call for many jobs. Tell us everything on your list when you call and we’ll talk it through."),
]
# Photo slots. To swap in a real photo: drop  assets/img/<name>-1600.webp + <name>-800.webp  into sitegen/assets/img,
# then set the slot's third value to "<name>" and rebuild. Alt text = the label.
SLOTS={
 "home":[("s-paint","Painting",None),("s-floor","Flooring & tile",None),("s-exterior","Pressure washing",None)],
 "about":[("a1","Interior finishes",None),("a2","Flooring",None),("a3","Decorative stone & tile",None),("a4","Pressure washing",None),("a5","Awnings & ornamental iron",None),("a6","Handyman jobs",None)],
 "interior":[("g-interior","Painting & plastering",None)],"remodel":[("g-remodel","Interior remodeling & handyman",None)],
 "floors-stone":[("g-floors","Floors, tile & stone",None)],"exterior":[("g-exterior","Pressure washing, awnings & iron",None)],
}
