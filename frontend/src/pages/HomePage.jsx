import { Link } from 'react-router-dom'
import useStudentStore from '../store/useStudentStore'

const features = [
  { icon: '🎯', title: 'Personalised Tests', desc: 'Diagnostic assessment identifies your weak topics. Every test is tailored to help you improve where it matters.' },
  { icon: '🤖', title: 'AI-Powered', desc: 'Google Gemini generates authentic CBSE-pattern questions with model answers and detailed evaluation.' },
  { icon: '📊', title: 'Instant Feedback', desc: 'Get topic-wise scores, error analysis, and a 4-week improvement plan the moment you submit.' },
  { icon: '📄', title: 'Offline Mode', desc: 'Download a print-ready PDF, write answers by hand, upload a scan, and get the same AI evaluation.' },
]

const classes = [
  { label: 'Class 10', subjects: ['Mathematics', 'Science', 'Social Science', 'English', 'Hindi'], color: 'blue' },
  { label: 'Class 12', subjects: ['Physics', 'Chemistry', 'Mathematics', 'Biology', 'Economics', 'Accountancy', 'Business Studies', 'English'], color: 'purple' },
]

export default function HomePage() {
  const { student } = useStudentStore()

  return (
    <div className="min-h-screen bg-white">
      {/* Navbar */}
      <nav className="sticky top-0 z-40 bg-white border-b border-gray-100 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-brand-600 rounded-lg flex items-center justify-center text-white font-bold text-sm">B</div>
          <span className="font-bold text-brand-900 text-lg">BoardAI</span>
        </div>
        <div className="flex items-center gap-3">
          {student ? (
            <Link to="/dashboard" className="btn-primary text-sm">Go to Dashboard →</Link>
          ) : (
            <Link to="/onboarding" className="btn-primary text-sm">Get Started Free →</Link>
          )}
        </div>
      </nav>

      {/* Hero */}
      <section className="text-center py-20 px-6 bg-gradient-to-br from-brand-50 to-white">
        <div className="inline-flex items-center gap-2 bg-brand-100 text-brand-700 text-xs font-semibold px-3 py-1 rounded-full mb-6">
          🇮🇳 Designed for CBSE Class 10 & 12 Students
        </div>
        <h1 className="text-4xl sm:text-5xl font-extrabold text-brand-900 leading-tight max-w-3xl mx-auto mb-6">
          AI Mock Tests Built Around <span className="text-brand-600">Your Weaknesses</span>
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto mb-10">
          Stop studying randomly. BoardAI analyses where you struggle, generates a CBSE-pattern mock test focused on those topics,
          evaluates your answers like an examiner, and tells you exactly how to improve.
        </p>
        <div className="flex flex-col sm:flex-row gap-3 justify-center">
          {student ? (
            <Link to="/dashboard" className="btn-primary text-base px-8 py-3">Open My Dashboard →</Link>
          ) : (
            <>
              <Link to="/onboarding" className="btn-primary text-base px-8 py-3">Create Free Profile →</Link>
              <a href="#how" className="btn-secondary text-base px-8 py-3">See How It Works</a>
            </>
          )}
        </div>
      </section>

      {/* Features */}
      <section className="py-16 px-6 max-w-6xl mx-auto">
        <h2 className="text-2xl font-bold text-center text-gray-800 mb-10">Everything you need to score higher</h2>
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((f) => (
            <div key={f.title} className="card hover:shadow-md transition-shadow">
              <div className="text-3xl mb-4">{f.icon}</div>
              <h3 className="font-semibold text-gray-800 mb-2">{f.title}</h3>
              <p className="text-sm text-gray-500 leading-relaxed">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* How it works */}
      <section id="how" className="py-16 px-6 bg-gray-50">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-2xl font-bold text-center text-gray-800 mb-12">How BoardAI Works</h2>
          <div className="space-y-8">
            {[
              { step: '01', title: 'Create Your Profile', desc: 'Enter your name, class (10 or 12), and select the subjects you want to practise.' },
              { step: '02', title: 'Complete Diagnostic', desc: 'Answer 7–10 short questions per subject about your confidence, topic strengths, and past performance.' },
              { step: '03', title: 'AI Generates Your Test', desc: 'Gemini + our CBSE knowledge base creates a full-length paper with extra focus on your weak topics.' },
              { step: '04', title: 'Take the Test', desc: 'Solve it online (timed, with autosave) or download a PDF to write on paper.' },
              { step: '05', title: 'Get Evaluated', desc: 'Submit your answers. AI grades every question, finds your mistakes, and creates a study plan.' },
            ].map((item) => (
              <div key={item.step} className="flex gap-6 items-start">
                <div className="shrink-0 w-12 h-12 bg-brand-600 text-white rounded-full flex items-center justify-center font-bold text-sm">
                  {item.step}
                </div>
                <div>
                  <h3 className="font-semibold text-gray-800 text-lg mb-1">{item.title}</h3>
                  <p className="text-gray-500 text-sm leading-relaxed">{item.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Subjects */}
      <section className="py-16 px-6 max-w-6xl mx-auto">
        <h2 className="text-2xl font-bold text-center text-gray-800 mb-10">Subjects Covered</h2>
        <div className="grid sm:grid-cols-2 gap-6">
          {classes.map((cls) => (
            <div key={cls.label} className={`card border-${cls.color}-200 bg-${cls.color}-50`}>
              <h3 className={`font-bold text-lg text-${cls.color}-800 mb-4`}>{cls.label}</h3>
              <div className="flex flex-wrap gap-2">
                {cls.subjects.map((s) => (
                  <span key={s} className={`badge badge-${cls.color === 'blue' ? 'blue' : 'gray'} text-xs`}>{s}</span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="py-16 px-6 bg-brand-600 text-white text-center">
        <h2 className="text-3xl font-bold mb-4">Ready to boost your CBSE score?</h2>
        <p className="text-brand-100 mb-8 max-w-md mx-auto">
          Join students across India using BoardAI to prepare smarter, not harder.
        </p>
        {!student && (
          <Link to="/onboarding" className="bg-white text-brand-600 font-semibold px-8 py-3 rounded-lg hover:bg-brand-50 transition-colors">
            Start Free →
          </Link>
        )}
      </section>

      <footer className="py-8 text-center text-sm text-gray-400 border-t">
        © 2025 BoardAI · For CBSE Class 10 & 12 · Built with Google Gemini AI
      </footer>
    </div>
  )
}
