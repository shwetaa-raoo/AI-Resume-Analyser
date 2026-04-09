import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class NLPMatcher:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words='english',
            ngram_range=(1, 2),  # Use unigrams and bigrams
            max_features=5000
        )
    
    def match_resume_to_job(self, resume_data, job):
        """
        Match resume against job description using NLP
        Returns match score and detailed analysis
        """
        try:
            # Prepare texts
            resume_text = self._prepare_resume_text(resume_data)
            job_text = self._prepare_job_text(job)
            
            # Calculate TF-IDF similarity
            tfidf_score = self._calculate_tfidf_similarity(resume_text, job_text)
            
            # Extract and compare skills
            resume_skills = self._extract_skills_list(resume_data.get('skills', ''))
            job_skills = self._extract_skills_list(job.required_skills)
            
            # Calculate skill match
            skill_match = self._calculate_skill_match(resume_skills, job_skills)
            
            # Calculate keyword match
            keyword_score = self._calculate_keyword_match(resume_text, job_text)
            
            # Weighted final score
            final_score = (
                tfidf_score * 0.35 +      # TF-IDF similarity weight
                skill_match['score'] * 0.45 +  # Skills match weight
                keyword_score * 0.20       # Keyword match weight
            )
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                skill_match, 
                resume_skills, 
                job_skills,
                final_score
            )
            
            return {
                'score': round(final_score, 2),
                'matched_skills': skill_match['matched'],
                'missing_skills': skill_match['missing'],
                'recommendations': recommendations,
                'breakdown': {
                    'tfidf_score': round(tfidf_score, 2),
                    'skill_score': round(skill_match['score'], 2),
                    'keyword_score': round(keyword_score, 2)
                }
            }
            
        except Exception as e:
            print(f"Error in NLP matching: {str(e)}")
            return {
                'score': 0,
                'matched_skills': [],
                'missing_skills': [],
                'recommendations': ['Error analyzing resume. Please try again.'],
                'breakdown': {
                    'tfidf_score': 0,
                    'skill_score': 0,
                    'keyword_score': 0
                }
            }
    
    def _prepare_resume_text(self, resume_data):
        """Combine all resume fields into single text"""
        text_parts = [
            resume_data.get('raw_text', ''),
            resume_data.get('skills', ''),
            resume_data.get('experience', ''),
            resume_data.get('education', '')
        ]
        return ' '.join(filter(None, text_parts))
    
    def _prepare_job_text(self, job):
        """Combine job fields into single text"""
        text_parts = [
            job.title,
            job.description,
            job.required_skills,
            job.experience or ''
        ]
        return ' '.join(filter(None, text_parts))
    
    def _calculate_tfidf_similarity(self, text1, text2):
        """Calculate TF-IDF cosine similarity between two texts"""
        try:
            tfidf_matrix = self.vectorizer.fit_transform([text1, text2])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return similarity * 100  # Convert to percentage
        except:
            return 0
    
    def _extract_skills_list(self, skills_text):
        """Convert comma-separated skills string to list"""
        if not skills_text:
            return []
        skills = [s.strip().lower() for s in skills_text.split(',')]
        return [s for s in skills if s]  # Remove empty strings
    
    def _calculate_skill_match(self, resume_skills, job_skills):
        """Calculate how many job skills are present in resume"""
        if not job_skills:
            return {'score': 50, 'matched': [], 'missing': []}
        
        resume_skills_set = set(resume_skills)
        job_skills_set = set(job_skills)
        
        # Find matched and missing skills
        matched_skills = []
        missing_skills = []
        
        for job_skill in job_skills_set:
            # Check for exact match or partial match
            is_matched = False
            for resume_skill in resume_skills_set:
                if (job_skill in resume_skill or resume_skill in job_skill or
                    self._are_similar_skills(job_skill, resume_skill)):
                    matched_skills.append(job_skill)
                    is_matched = True
                    break
            
            if not is_matched:
                missing_skills.append(job_skill)
        
        # Calculate score
        if len(job_skills_set) > 0:
            score = (len(matched_skills) / len(job_skills_set)) * 100
        else:
            score = 50  # Default score if no required skills
        
        return {
            'score': score,
            'matched': list(set(matched_skills)),
            'missing': list(set(missing_skills))
        }
    
    def _are_similar_skills(self, skill1, skill2):
        """Check if two skills are similar (e.g., 'js' and 'javascript')"""
        skill_synonyms = {
            'js': 'javascript',
            'ts': 'typescript',
            'py': 'python',
            'ml': 'machine learning',
            'ai': 'artificial intelligence',
            'db': 'database',
            'react.js': 'react',
            'node': 'node.js',
            'vue.js': 'vue',
            'angular.js': 'angular'
        }
        
        skill1 = skill1.lower().strip()
        skill2 = skill2.lower().strip()
        
        # Check direct synonyms
        if skill1 in skill_synonyms and skill_synonyms[skill1] == skill2:
            return True
        if skill2 in skill_synonyms and skill_synonyms[skill2] == skill1:
            return True
        
        return False
    
    def _calculate_keyword_match(self, resume_text, job_text):
        """Calculate keyword overlap between resume and job"""
        # Extract keywords from job description
        job_keywords = self._extract_keywords(job_text)
        resume_text_lower = resume_text.lower()
        
        # Count how many keywords appear in resume
        matched_count = 0
        for keyword in job_keywords:
            if keyword in resume_text_lower:
                matched_count += 1
        
        if len(job_keywords) > 0:
            return (matched_count / len(job_keywords)) * 100
        return 50
    
    def _extract_keywords(self, text):
        """Extract important keywords from text"""
        # Remove common words and extract unique terms
        words = re.findall(r'\b[a-z]{3,}\b', text.lower())
        
        # Remove very common words
        stop_words = {'the', 'and', 'for', 'with', 'this', 'that', 'from', 'have',
                     'will', 'are', 'you', 'can', 'our', 'more', 'about', 'into',
                     'through', 'than', 'only', 'some', 'could', 'other'}
        
        keywords = [w for w in words if w not in stop_words]
        
        # Return unique keywords
        return list(set(keywords))[:50]  # Limit to top 50 keywords
    
    def _generate_recommendations(self, skill_match, resume_skills, job_skills, score):
        """Generate personalized recommendations"""
        recommendations = []
        
        # Score-based recommendations
        if score >= 80:
            recommendations.append("Excellent match! Your profile aligns very well with this position.")
        elif score >= 60:
            recommendations.append("Good match! Consider highlighting your relevant experience in your cover letter.")
        elif score >= 40:
            recommendations.append("Moderate match. Focus on demonstrating transferable skills.")
        else:
            recommendations.append("Limited match. Consider gaining more relevant experience for this role.")
        
        # Missing skills recommendations
        if skill_match['missing']:
            missing_count = len(skill_match['missing'])
            if missing_count <= 3:
                skills_str = ', '.join(skill_match['missing'][:3])
                recommendations.append(f"Consider adding these skills to your resume: {skills_str}")
            elif missing_count <= 6:
                skills_str = ', '.join(skill_match['missing'][:5])
                recommendations.append(f"You're missing several key skills: {skills_str}")
                recommendations.append("Consider taking online courses to learn these skills.")
            else:
                recommendations.append(f"You're missing {missing_count} required skills. This role may require significant upskilling.")
        
        # Matched skills recommendations
        if skill_match['matched']:
            matched_count = len(skill_match['matched'])
            if matched_count >= 5:
                recommendations.append(f"Great! You have {matched_count} matching skills. Make sure these are prominent in your resume.")
            elif matched_count >= 3:
                recommendations.append("You have several matching skills. Emphasize these in your application.")
        
        # General tips
        if score < 70:
            recommendations.append("Tip: Customize your resume to include keywords from the job description.")
            recommendations.append("Tip: Quantify your achievements with specific numbers and metrics.")
        
        return recommendations[:6]  # Return top 6 recommendations
