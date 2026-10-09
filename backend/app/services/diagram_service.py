import html
from typing import Optional, Dict, Any
from ..models import DiagramData

class DiagramService:
    @staticmethod
    def get_diagram_for_topic(topic: str) -> Optional[DiagramData]:
        topic_lower = topic.lower()
        
        # 1. PN Junction Diode
        if any(k in topic_lower for k in ["pn junction", "p-n junction", "diode", "semiconductor junction", "depletion region"]):
            return DiagramData(
                type="circuit",
                title="P-N Junction Diode in Thermal Equilibrium",
                description="Visual schematic of a PN Junction Diode illustrating P-type region (majority holes), N-type region (majority electrons), and the central Depletion Layer with internal barrier electric field.",
                labels=["P-Type (Holes +)", "Depletion Region (W)", "N-Type (Electrons -)", "Built-in Barrier Potential (Vbi)", "Anode (+)", "Cathode (-)"],
                svg_content="""<svg viewBox="0 0 760 340" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); border-radius: 12px; font-family: system-ui, -apple-system, sans-serif;">
  <defs>
    <linearGradient id="pGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#3b82f6" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#2563eb" stop-opacity="0.9"/>
    </linearGradient>
    <linearGradient id="nGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#10b981" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#059669" stop-opacity="0.9"/>
    </linearGradient>
    <linearGradient id="depGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#f59e0b" stop-opacity="0.7"/>
      <stop offset="50%" stop-color="#ef4444" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#f59e0b" stop-opacity="0.7"/>
    </linearGradient>
    <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#facc15"/>
    </marker>
  </defs>

  <!-- Title -->
  <text x="380" y="36" fill="#f8fafc" font-size="18" font-weight="700" text-anchor="middle">P-N Junction Diode Structure &amp; Depletion Layer</text>

  <!-- P-Region Box -->
  <rect x="80" y="65" width="220" height="180" rx="8" fill="url(#pGrad)" stroke="#60a5fa" stroke-width="2"/>
  <text x="190" y="98" fill="#ffffff" font-size="16" font-weight="700" text-anchor="middle">P-Type Semiconductor</text>
  <text x="190" y="118" fill="#bfdbfe" font-size="12" text-anchor="middle">Majority: Holes (⊕)</text>

  <!-- Holes particles -->
  <g fill="#bfdbfe" font-size="14" font-weight="bold">
    <circle cx="120" cy="150" r="12" fill="#1e3a8a" stroke="#93c5fd" stroke-width="2"/><text x="120" y="155" fill="#ffffff" text-anchor="middle">+</text>
    <circle cx="170" cy="150" r="12" fill="#1e3a8a" stroke="#93c5fd" stroke-width="2"/><text x="170" y="155" fill="#ffffff" text-anchor="middle">+</text>
    <circle cx="220" cy="150" r="12" fill="#1e3a8a" stroke="#93c5fd" stroke-width="2"/><text x="220" y="155" fill="#ffffff" text-anchor="middle">+</text>
    <circle cx="140" cy="195" r="12" fill="#1e3a8a" stroke="#93c5fd" stroke-width="2"/><text x="140" y="200" fill="#ffffff" text-anchor="middle">+</text>
    <circle cx="190" cy="195" r="12" fill="#1e3a8a" stroke="#93c5fd" stroke-width="2"/><text x="190" y="200" fill="#ffffff" text-anchor="middle">+</text>
    <circle cx="240" cy="195" r="12" fill="#1e3a8a" stroke="#93c5fd" stroke-width="2"/><text x="240" y="200" fill="#ffffff" text-anchor="middle">+</text>
  </g>

  <!-- Depletion Region -->
  <rect x="300" y="65" width="160" height="180" fill="url(#depGrad)" stroke="#f87171" stroke-width="2" stroke-dasharray="4,4"/>
  <text x="380" y="98" fill="#fef08a" font-size="15" font-weight="700" text-anchor="middle">Depletion Region</text>
  <text x="380" y="118" fill="#fee2e2" font-size="11" text-anchor="middle">Immobile Ions (No Free Carriers)</text>

  <!-- Immobile Ions in Depletion -->
  <g font-size="13" font-weight="bold">
    <!-- Negative acceptor ions in P side of depletion -->
    <circle cx="340" cy="150" r="12" fill="#7f1d1d" stroke="#fca5a5" stroke-width="2"/><text x="340" y="154" fill="#ffffff" text-anchor="middle">−</text>
    <circle cx="340" cy="195" r="12" fill="#7f1d1d" stroke="#fca5a5" stroke-width="2"/><text x="340" y="199" fill="#ffffff" text-anchor="middle">−</text>
    <!-- Positive donor ions in N side of depletion -->
    <circle cx="420" cy="150" r="12" fill="#78350f" stroke="#fde047" stroke-width="2"/><text x="420" y="154" fill="#ffffff" text-anchor="middle">+</text>
    <circle cx="420" cy="195" r="12" fill="#78350f" stroke="#fde047" stroke-width="2"/><text x="420" y="199" fill="#ffffff" text-anchor="middle">+</text>
  </g>

  <!-- Internal Electric Field Arrow -->
  <line x1="420" y1="225" x2="340" y2="225" stroke="#facc15" stroke-width="3" marker-end="url(#arrow)"/>
  <text x="380" y="240" fill="#facc15" font-size="11" font-weight="bold" text-anchor="middle">E-Field (N → P)</text>

  <!-- N-Region Box -->
  <rect x="460" y="65" width="220" height="180" rx="8" fill="url(#nGrad)" stroke="#34d399" stroke-width="2"/>
  <text x="570" y="98" fill="#ffffff" font-size="16" font-weight="700" text-anchor="middle">N-Type Semiconductor</text>
  <text x="570" y="118" fill="#a7f3d0" font-size="12" text-anchor="middle">Majority: Electrons (e⁻)</text>

  <!-- Electrons particles -->
  <g fill="#a7f3d0" font-size="14" font-weight="bold">
    <circle cx="500" cy="150" r="12" fill="#064e3b" stroke="#6ee7b7" stroke-width="2"/><text x="500" y="154" fill="#ffffff" text-anchor="middle">−</text>
    <circle cx="550" cy="150" r="12" fill="#064e3b" stroke="#6ee7b7" stroke-width="2"/><text x="550" y="154" fill="#ffffff" text-anchor="middle">−</text>
    <circle cx="600" cy="150" r="12" fill="#064e3b" stroke="#6ee7b7" stroke-width="2"/><text x="600" y="154" fill="#ffffff" text-anchor="middle">−</text>
    <circle cx="520" cy="195" r="12" fill="#064e3b" stroke="#6ee7b7" stroke-width="2"/><text x="520" y="199" fill="#ffffff" text-anchor="middle">−</text>
    <circle cx="570" cy="195" r="12" fill="#064e3b" stroke="#6ee7b7" stroke-width="2"/><text x="570" y="199" fill="#ffffff" text-anchor="middle">−</text>
    <circle cx="620" cy="195" r="12" fill="#064e3b" stroke="#6ee7b7" stroke-width="2"/><text x="620" y="199" fill="#ffffff" text-anchor="middle">−</text>
  </g>

  <!-- Terminals -->
  <line x1="30" y1="155" x2="80" y2="155" stroke="#94a3b8" stroke-width="4"/>
  <circle cx="30" cy="155" r="6" fill="#38bdf8"/>
  <text x="25" y="185" fill="#38bdf8" font-size="14" font-weight="bold" text-anchor="middle">Anode (+)</text>

  <line x1="680" y1="155" x2="730" y2="155" stroke="#94a3b8" stroke-width="4"/>
  <circle cx="730" cy="155" r="6" fill="#34d399"/>
  <text x="735" y="185" fill="#34d399" font-size="14" font-weight="bold" text-anchor="middle">Cathode (-)</text>

  <!-- Legend Bottom -->
  <rect x="140" y="275" width="480" height="45" rx="6" fill="#1e293b" stroke="#334155" stroke-width="1"/>
  <text x="380" y="302" fill="#cbd5e1" font-size="13" text-anchor="middle">⚡ Forward Bias reduces barrier (Current flows) | 🛑 Reverse Bias widens barrier</text>
</svg>"""
            )

        # 2. Photosynthesis
        if any(k in topic_lower for k in ["photosynthesis", "chlorophyll", "chloroplast", "plant cell", "light reaction"]):
            return DiagramData(
                type="concept_map",
                title="The Photosynthesis Process & Chemical Equation",
                description="Labelled diagram of Photosynthesis showing Sunlight, Carbon Dioxide, and Water being converted into Glucose and Oxygen inside the Chloroplast.",
                labels=["Sunlight (Photons)", "Carbon Dioxide (6 CO₂)", "Water (6 H₂O)", "Chloroplast (Chlorophyll)", "Glucose (C₆H₁₂O₆)", "Oxygen (6 O₂)"],
                svg_content="""<svg viewBox="0 0 760 360" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background: linear-gradient(135deg, #064e3b 0%, #022c22 100%); border-radius: 12px; font-family: system-ui, -apple-system, sans-serif;">
  <!-- Title -->
  <text x="380" y="38" fill="#f0fdf4" font-size="20" font-weight="700" text-anchor="middle">Photosynthesis: Inputs, Processing &amp; Outputs</text>

  <!-- Sun -->
  <circle cx="110" cy="95" r="35" fill="#f59e0b" stroke="#fde047" stroke-width="4"/>
  <text x="110" y="100" fill="#78350f" font-size="12" font-weight="bold" text-anchor="middle">SUNLIGHT</text>
  <line x1="145" y1="110" x2="250" y2="160" stroke="#facc15" stroke-width="3" stroke-dasharray="5,5"/>

  <!-- Plant/Chloroplast Central Hub -->
  <rect x="250" y="110" width="260" height="160" rx="20" fill="#15803d" stroke="#86efac" stroke-width="3"/>
  <text x="380" y="150" fill="#ffffff" font-size="18" font-weight="bold" text-anchor="middle">🌿 CHLOROPLAST</text>
  <text x="380" y="180" fill="#bbf7d0" font-size="13" text-anchor="middle">Site of Light &amp; Dark Reactions</text>
  <text x="380" y="205" fill="#dcfce7" font-size="12" text-anchor="middle">(Chlorophyll absorbs blue/red light)</text>

  <!-- Inputs Left -->
  <g fill="#ffffff" font-size="13" font-weight="600">
    <!-- CO2 -->
    <rect x="50" y="165" width="150" height="42" rx="8" fill="#334155" stroke="#94a3b8"/>
    <text x="125" y="191" text-anchor="middle">Carbon Dioxide (6CO₂)</text>
    <line x1="200" y1="186" x2="250" y2="186" stroke="#94a3b8" stroke-width="2"/>

    <!-- Water H2O -->
    <rect x="50" y="225" width="150" height="42" rx="8" fill="#0284c7" stroke="#38bdf8"/>
    <text x="125" y="251" text-anchor="middle">Water (6H₂O) from Roots</text>
    <line x1="200" y1="246" x2="250" y2="246" stroke="#38bdf8" stroke-width="2"/>
  </g>

  <!-- Outputs Right -->
  <g fill="#ffffff" font-size="13" font-weight="600">
    <!-- Glucose -->
    <rect x="560" y="140" width="160" height="50" rx="8" fill="#b45309" stroke="#fde047"/>
    <text x="640" y="165" text-anchor="middle">Glucose (C₆H₁₂O₆)</text>
    <text x="640" y="182" fill="#fef08a" font-size="11" text-anchor="middle">(Plant Food &amp; Energy)</text>
    <line x1="510" y1="165" x2="560" y2="165" stroke="#fde047" stroke-width="3"/>

    <!-- Oxygen -->
    <rect x="560" y="215" width="160" height="50" rx="8" fill="#047857" stroke="#34d399"/>
    <text x="640" y="240" text-anchor="middle">Oxygen (6O₂)</text>
    <text x="640" y="257" fill="#a7f3d0" font-size="11" text-anchor="middle">(Released to Atmosphere)</text>
    <line x1="510" y1="240" x2="560" y2="240" stroke="#34d399" stroke-width="3"/>
  </g>

  <!-- Chemical Equation Footer -->
  <rect x="80" y="295" width="600" height="45" rx="8" fill="#065f46" stroke="#10b981" stroke-width="1.5"/>
  <text x="380" y="323" fill="#ffffff" font-size="15" font-weight="bold" text-anchor="middle">Equation: 6 CO₂ + 6 H₂O + Light ➔ C₆H₁₂O₆ + 6 O₂</text>
</svg>"""
            )

        # 3. Neural Network
        if any(k in topic_lower for k in ["neural network", "deep learning", "perceptron", "artificial intelligence", "machine learning", "hidden layer"]):
            return DiagramData(
                type="flowchart",
                title="Artificial Neural Network Architecture (Multi-Layer Perceptron)",
                description="Visual diagram of an artificial neural network with Input Layer, Weighted Hidden Layers, Activation Functions, and Output Layer.",
                labels=["Input Layer (x₁, x₂, x₃)", "Hidden Layer 1 (Weights w + Bias b)", "Hidden Layer 2", "Output Layer (ŷ)", "Backpropagation Flow"],
                svg_content="""<svg viewBox="0 0 760 360" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background: linear-gradient(135deg, #090d16 0%, #1e1e38 100%); border-radius: 12px; font-family: system-ui, -apple-system, sans-serif;">
  <text x="380" y="35" fill="#f8fafc" font-size="19" font-weight="700" text-anchor="middle">Multi-Layer Neural Network Architecture</text>

  <!-- Connections / Synaptic weights -->
  <g stroke="#3b82f6" stroke-opacity="0.3" stroke-width="1.5">
    <!-- Input to Hidden 1 -->
    <line x1="120" y1="90" x2="280" y2="70"/><line x1="120" y1="90" x2="280" y2="140"/><line x1="120" y1="90" x2="280" y2="210"/><line x1="120" y1="90" x2="280" y2="280"/>
    <line x1="120" y1="170" x2="280" y2="70"/><line x1="120" y1="170" x2="280" y2="140"/><line x1="120" y1="170" x2="280" y2="210"/><line x1="120" y1="170" x2="280" y2="280"/>
    <line x1="120" y1="250" x2="280" y2="70"/><line x1="120" y1="250" x2="280" y2="140"/><line x1="120" y1="250" x2="280" y2="210"/><line x1="120" y1="250" x2="280" y2="280"/>
    <!-- Hidden 1 to Hidden 2 -->
    <line x1="280" y1="70" x2="460" y2="90"/><line x1="280" y1="70" x2="460" y2="170"/><line x1="280" y1="70" x2="460" y2="250"/>
    <line x1="280" y1="140" x2="460" y2="90"/><line x1="280" y1="140" x2="460" y2="170"/><line x1="280" y1="140" x2="460" y2="250"/>
    <line x1="280" y1="210" x2="460" y2="90"/><line x1="280" y1="210" x2="460" y2="170"/><line x1="280" y1="210" x2="460" y2="250"/>
    <line x1="280" y1="280" x2="460" y2="90"/><line x1="280" y1="280" x2="460" y2="170"/><line x1="280" y1="280" x2="460" y2="250"/>
    <!-- Hidden 2 to Output -->
    <line x1="460" y1="90" x2="620" y2="135"/><line x1="460" y1="90" x2="620" y2="215"/>
    <line x1="460" y1="170" x2="620" y2="135"/><line x1="460" y1="170" x2="620" y2="215"/>
    <line x1="460" y1="250" x2="620" y2="135"/><line x1="460" y1="250" x2="620" y2="215"/>
  </g>

  <!-- Input Layer -->
  <g>
    <text x="120" y="325" fill="#93c5fd" font-size="13" font-weight="bold" text-anchor="middle">Input Layer</text>
    <circle cx="120" cy="90" r="20" fill="#1e3a8a" stroke="#60a5fa" stroke-width="2.5"/><text x="120" y="95" fill="#ffffff" font-size="12" font-weight="bold" text-anchor="middle">x₁</text>
    <circle cx="120" cy="170" r="20" fill="#1e3a8a" stroke="#60a5fa" stroke-width="2.5"/><text x="120" y="175" fill="#ffffff" font-size="12" font-weight="bold" text-anchor="middle">x₂</text>
    <circle cx="120" cy="250" r="20" fill="#1e3a8a" stroke="#60a5fa" stroke-width="2.5"/><text x="120" y="255" fill="#ffffff" font-size="12" font-weight="bold" text-anchor="middle">x₃</text>
  </g>

  <!-- Hidden Layer 1 -->
  <g>
    <text x="280" y="325" fill="#c084fc" font-size="13" font-weight="bold" text-anchor="middle">Hidden 1</text>
    <circle cx="280" cy="70" r="18" fill="#581c87" stroke="#c084fc" stroke-width="2"/><text x="280" y="75" fill="#ffffff" font-size="11" text-anchor="middle">h₁</text>
    <circle cx="280" cy="140" r="18" fill="#581c87" stroke="#c084fc" stroke-width="2"/><text x="280" y="145" fill="#ffffff" font-size="11" text-anchor="middle">h₂</text>
    <circle cx="280" cy="210" r="18" fill="#581c87" stroke="#c084fc" stroke-width="2"/><text x="280" y="215" fill="#ffffff" font-size="11" text-anchor="middle">h₃</text>
    <circle cx="280" cy="280" r="18" fill="#581c87" stroke="#c084fc" stroke-width="2"/><text x="280" y="285" fill="#ffffff" font-size="11" text-anchor="middle">h₄</text>
  </g>

  <!-- Hidden Layer 2 -->
  <g>
    <text x="460" y="325" fill="#f472b6" font-size="13" font-weight="bold" text-anchor="middle">Hidden 2</text>
    <circle cx="460" cy="90" r="18" fill="#831843" stroke="#f472b6" stroke-width="2"/><text x="460" y="95" fill="#ffffff" font-size="11" text-anchor="middle">a₁</text>
    <circle cx="460" cy="170" r="18" fill="#831843" stroke="#f472b6" stroke-width="2"/><text x="460" y="175" fill="#ffffff" font-size="11" text-anchor="middle">a₂</text>
    <circle cx="460" cy="250" r="18" fill="#831843" stroke="#f472b6" stroke-width="2"/><text x="460" y="255" fill="#ffffff" font-size="11" text-anchor="middle">a₃</text>
  </g>

  <!-- Output Layer -->
  <g>
    <text x="620" y="325" fill="#34d399" font-size="13" font-weight="bold" text-anchor="middle">Output Layer</text>
    <circle cx="620" cy="135" r="22" fill="#064e3b" stroke="#34d399" stroke-width="2.5"/><text x="620" y="140" fill="#ffffff" font-size="12" font-weight="bold" text-anchor="middle">ŷ₁</text>
    <circle cx="620" cy="215" r="22" fill="#064e3b" stroke="#34d399" stroke-width="2.5"/><text x="620" y="220" fill="#ffffff" font-size="12" font-weight="bold" text-anchor="middle">ŷ₂</text>
  </g>

  <!-- Feedforward / Backprop note -->
  <text x="380" y="348" fill="#94a3b8" font-size="12" text-anchor="middle">Forward Pass: z = W · x + b, a = σ(z) ➔ Loss ➔ Backpropagation adjusts weights W</text>
</svg>"""
            )

        # 4. Water Cycle
        if any(k in topic_lower for k in ["water cycle", "hydrologic cycle", "evaporation", "precipitation", "condensation"]):
            return DiagramData(
                type="concept_map",
                title="The Hydrological (Water) Cycle",
                description="Diagram showing the continuous movement of water on, above, and below the surface of the Earth.",
                labels=["Evaporation (Heat from Sun)", "Condensation (Cloud formation)", "Precipitation (Rain / Snow)", "Transpiration (Plants)", "Surface Runoff & Infiltration"],
                svg_content="""<svg viewBox="0 0 760 360" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background: linear-gradient(180deg, #0284c7 0%, #0369a1 40%, #064e3b 80%, #15803d 100%); border-radius: 12px; font-family: system-ui, -apple-system, sans-serif;">
  <text x="380" y="34" fill="#ffffff" font-size="20" font-weight="700" text-anchor="middle">The Earth's Water Cycle</text>
  
  <!-- Sun -->
  <circle cx="660" cy="80" r="35" fill="#f59e0b" stroke="#fde047" stroke-width="4"/>
  <text x="660" y="85" fill="#78350f" font-size="12" font-weight="bold" text-anchor="middle">SUN</text>

  <!-- Clouds (Condensation) -->
  <g fill="#f8fafc" opacity="0.95">
    <ellipse cx="260" cy="90" rx="45" ry="25"/>
    <ellipse cx="300" cy="80" rx="40" ry="30"/>
    <ellipse cx="340" cy="95" rx="35" ry="22"/>
  </g>
  <text x="300" y="60" fill="#ffffff" font-size="14" font-weight="bold" text-anchor="middle">2. CONDENSATION</text>
  <text x="300" y="125" fill="#e2e8f0" font-size="11" text-anchor="middle">(Vapor cools to clouds)</text>

  <!-- Evaporation arrows -->
  <g stroke="#facc15" stroke-width="3" stroke-dasharray="4,4">
    <line x1="560" y1="240" x2="560" y2="140"/>
    <line x1="590" y1="240" x2="590" y2="150"/>
  </g>
  <text x="580" y="195" fill="#fef08a" font-size="14" font-weight="bold" text-anchor="middle">1. EVAPORATION</text>
  <text x="580" y="215" fill="#ffffff" font-size="11" text-anchor="middle">(Sun heats ocean water)</text>

  <!-- Precipitation (Rain) -->
  <g stroke="#38bdf8" stroke-width="2" stroke-dasharray="6,6">
    <line x1="240" y1="120" x2="220" y2="200"/>
    <line x1="270" y1="120" x2="250" y2="200"/>
    <line x1="300" y1="120" x2="280" y2="200"/>
  </g>
  <text x="220" y="150" fill="#bae6fd" font-size="14" font-weight="bold" text-anchor="middle">3. PRECIPITATION</text>
  <text x="220" y="170" fill="#ffffff" font-size="11" text-anchor="middle">(Rain, Snow)</text>

  <!-- Mountains & River -->
  <polygon points="80,310 180,180 280,310" fill="#475569"/>
  <polygon points="150,220 180,180 210,220" fill="#f8fafc"/>
  
  <!-- Ocean / Water body -->
  <rect x="420" y="260" width="320" height="90" fill="#0284c7" opacity="0.9"/>
  <text x="580" y="305" fill="#e0f2fe" font-size="16" font-weight="bold" text-anchor="middle">Ocean / Lake</text>

  <!-- Runoff arrow -->
  <text x="320" y="285" fill="#ffffff" font-size="13" font-weight="bold">4. Surface Runoff &amp; Infiltration ➔</text>
</svg>"""
            )

        # 5. Generic Concept Visual / Process Flow for other topics
        return DiagramData(
            type="flowchart",
            title=f"Conceptual Flow: {topic.title()}",
            description=f"Structured visual mapping demonstrating the core phases, inputs, operations, and outcomes of {topic}.",
            labels=["1. Foundation & Input", "2. Core Processing / Rule", "3. State Transformation", "4. Outcome & Application"],
            svg_content=f"""<svg viewBox="0 0 760 260" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); border-radius: 12px; font-family: system-ui, -apple-system, sans-serif;">
  <text x="380" y="35" fill="#f8fafc" font-size="18" font-weight="700" text-anchor="middle">{html.escape(topic.title())} — Conceptual Architecture</text>
  
  <!-- Flow Blocks -->
  <!-- Step 1 -->
  <rect x="50" y="80" width="140" height="90" rx="10" fill="#1e3a8a" stroke="#60a5fa" stroke-width="2"/>
  <text x="120" y="115" fill="#93c5fd" font-size="12" font-weight="bold" text-anchor="middle">PHASE 1</text>
  <text x="120" y="138" fill="#ffffff" font-size="14" font-weight="bold" text-anchor="middle">Input / Basis</text>
  <text x="120" y="155" fill="#cbd5e1" font-size="10" text-anchor="middle">Core Principles</text>

  <!-- Arrow 1 -->
  <line x1="190" y1="125" x2="230" y2="125" stroke="#38bdf8" stroke-width="3"/>
  <polygon points="230,120 240,125 230,130" fill="#38bdf8"/>

  <!-- Step 2 -->
  <rect x="240" y="80" width="140" height="90" rx="10" fill="#4c1d95" stroke="#c084fc" stroke-width="2"/>
  <text x="310" y="115" fill="#e9d5ff" font-size="12" font-weight="bold" text-anchor="middle">PHASE 2</text>
  <text x="310" y="138" fill="#ffffff" font-size="14" font-weight="bold" text-anchor="middle">Processing</text>
  <text x="310" y="155" fill="#cbd5e1" font-size="10" text-anchor="middle">Mechanism</text>

  <!-- Arrow 2 -->
  <line x1="380" y1="125" x2="420" y2="125" stroke="#c084fc" stroke-width="3"/>
  <polygon points="420,120 430,125 420,130" fill="#c084fc"/>

  <!-- Step 3 -->
  <rect x="430" y="80" width="140" height="90" rx="10" fill="#831843" stroke="#f472b6" stroke-width="2"/>
  <text x="500" y="115" fill="#fce7f3" font-size="12" font-weight="bold" text-anchor="middle">PHASE 3</text>
  <text x="500" y="138" fill="#ffffff" font-size="14" font-weight="bold" text-anchor="middle">Execution</text>
  <text x="500" y="155" fill="#cbd5e1" font-size="10" text-anchor="middle">Transformation</text>

  <!-- Arrow 3 -->
  <line x1="570" y1="125" x2="610" y2="125" stroke="#f472b6" stroke-width="3"/>
  <polygon points="610,120 620,125 610,130" fill="#f472b6"/>

  <!-- Step 4 -->
  <rect x="620" y="80" width="110" height="90" rx="10" fill="#064e3b" stroke="#34d399" stroke-width="2"/>
  <text x="675" y="115" fill="#a7f3d0" font-size="12" font-weight="bold" text-anchor="middle">PHASE 4</text>
  <text x="675" y="138" fill="#ffffff" font-size="14" font-weight="bold" text-anchor="middle">Results</text>
  <text x="675" y="155" fill="#cbd5e1" font-size="10" text-anchor="middle">Application</text>

  <!-- Summary Note -->
  <text x="380" y="215" fill="#94a3b8" font-size="13" text-anchor="middle">Interactive dynamic representation for {html.escape(topic)}. Ready for real-world application.</text>
</svg>"""
        )
