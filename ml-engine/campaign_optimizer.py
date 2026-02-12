"""
ML Engine - AI-Powered Campaign Optimization
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from typing import Dict, List, Any, Tuple
import joblib
import json
from datetime import datetime
from loguru import logger


class CampaignOptimizer:
    """AI model for optimizing campaign performance"""
    
    def __init__(self):
        self.roas_model = None
        self.conversion_model = None
        self.scaler = StandardScaler()
        self.feature_names = [
            'daily_budget', 'bid_amount', 'target_cpa', 'target_roas',
            'impressions', 'clicks', 'ctr', 'cpc', 'days_running'
        ]
    
    def prepare_features(self, campaign_data: Dict[str, Any]) -> np.ndarray:
        """Prepare features for model input"""
        features = []
        for feature in self.feature_names:
            features.append(campaign_data.get(feature, 0))
        return np.array(features).reshape(1, -1)
    
    def train_roas_model(self, training_data: pd.DataFrame) -> Dict[str, float]:
        """Train ROAS prediction model"""
        logger.info("Training ROAS prediction model...")
        
        # Prepare features and target
        X = training_data[self.feature_names]
        y = training_data['roas']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.roas_model = GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
        self.roas_model.fit(X_train_scaled, y_train)
        
        # Evaluate
        train_score = self.roas_model.score(X_train_scaled, y_train)
        test_score = self.roas_model.score(X_test_scaled, y_test)
        
        metrics = {
            'train_r2': train_score,
            'test_r2': test_score,
            'n_samples': len(X_train)
        }
        
        logger.info(f"ROAS model trained: R²={test_score:.3f}")
        return metrics
    
    def train_conversion_model(self, training_data: pd.DataFrame) -> Dict[str, float]:
        """Train conversion prediction model"""
        logger.info("Training conversion prediction model...")
        
        X = training_data[self.feature_names]
        y = training_data['conversions']
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        self.conversion_model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.conversion_model.fit(X_train_scaled, y_train)
        
        train_score = self.conversion_model.score(X_train_scaled, y_train)
        test_score = self.conversion_model.score(X_test_scaled, y_test)
        
        metrics = {
            'train_r2': train_score,
            'test_r2': test_score,
            'n_samples': len(X_train)
        }
        
        logger.info(f"Conversion model trained: R²={test_score:.3f}")
        return metrics
    
    def predict_roas(self, campaign_data: Dict[str, Any]) -> Tuple[float, float]:
        """Predict ROAS for campaign"""
        if self.roas_model is None:
            raise ValueError("ROAS model not trained")
        
        features = self.prepare_features(campaign_data)
        features_scaled = self.scaler.transform(features)
        
        predicted_roas = self.roas_model.predict(features_scaled)[0]
        
        # Calculate confidence (simplified)
        confidence = min(0.95, self.roas_model.score(features_scaled, [predicted_roas]))
        
        return predicted_roas, confidence
    
    def predict_conversions(self, campaign_data: Dict[str, Any]) -> int:
        """Predict conversions for campaign"""
        if self.conversion_model is None:
            raise ValueError("Conversion model not trained")
        
        features = self.prepare_features(campaign_data)
        features_scaled = self.scaler.transform(features)
        
        predicted_conversions = self.conversion_model.predict(features_scaled)[0]
        return max(0, int(predicted_conversions))
    
    def recommend_budget(self, campaign_data: Dict[str, Any], target_roas: float) -> float:
        """Recommend optimal budget allocation"""
        current_budget = campaign_data.get('daily_budget', 0)
        current_roas = campaign_data.get('roas', 0)
        
        if current_roas >= target_roas:
            # Performing well, suggest 20% increase
            recommended_budget = current_budget * 1.2
        elif current_roas >= target_roas * 0.8:
            # Close to target, suggest 10% increase
            recommended_budget = current_budget * 1.1
        elif current_roas >= target_roas * 0.5:
            # Below target, maintain budget
            recommended_budget = current_budget
        else:
            # Far below target, suggest 20% decrease
            recommended_budget = current_budget * 0.8
        
        return round(recommended_budget, 2)
    
    def generate_recommendations(self, campaign_data: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        ctr = campaign_data.get('ctr', 0)
        cpc = campaign_data.get('cpc', 0)
        roas = campaign_data.get('roas', 0)
        target_roas = campaign_data.get('target_roas', 3.0)
        
        # CTR recommendations
        if ctr < 1.0:
            recommendations.append("Low CTR detected. Consider improving ad creatives and headlines.")
        elif ctr > 3.0:
            recommendations.append("Excellent CTR! Consider scaling this campaign.")
        
        # CPC recommendations
        if cpc > 5.0:
            recommendations.append("High CPC detected. Review targeting and bidding strategy.")
        
        # ROAS recommendations
        if roas < target_roas * 0.5:
            recommendations.append("ROAS significantly below target. Consider pausing campaign or major optimization.")
        elif roas < target_roas:
            recommendations.append("ROAS below target. Optimize targeting, creatives, or landing pages.")
        elif roas > target_roas * 1.5:
            recommendations.append("Excellent ROAS! Consider increasing budget to scale.")
        
        # Budget recommendations
        daily_budget = campaign_data.get('daily_budget', 0)
        recommended_budget = self.recommend_budget(campaign_data, target_roas)
        if recommended_budget > daily_budget:
            recommendations.append(f"Increase daily budget to ${recommended_budget:.2f} for better results.")
        elif recommended_budget < daily_budget:
            recommendations.append(f"Decrease daily budget to ${recommended_budget:.2f} to improve efficiency.")
        
        if not recommendations:
            recommendations.append("Campaign is performing well. Continue monitoring.")
        
        return recommendations
    
    def save_models(self, path: str = "./ml-engine/models"):
        """Save trained models to disk"""
        import os
        os.makedirs(path, exist_ok=True)
        
        if self.roas_model:
            joblib.dump(self.roas_model, f"{path}/roas_model.pkl")
        if self.conversion_model:
            joblib.dump(self.conversion_model, f"{path}/conversion_model.pkl")
        joblib.dump(self.scaler, f"{path}/scaler.pkl")
        
        logger.info(f"Models saved to {path}")
    
    def load_models(self, path: str = "./ml-engine/models"):
        """Load trained models from disk"""
        import os
        
        if os.path.exists(f"{path}/roas_model.pkl"):
            self.roas_model = joblib.load(f"{path}/roas_model.pkl")
        if os.path.exists(f"{path}/conversion_model.pkl"):
            self.conversion_model = joblib.load(f"{path}/conversion_model.pkl")
        if os.path.exists(f"{path}/scaler.pkl"):
            self.scaler = joblib.load(f"{path}/scaler.pkl")
        
        logger.info(f"Models loaded from {path}")


class BudgetOptimizer:
    """Optimize budget allocation across campaigns"""
    
    @staticmethod
    def optimize_portfolio(campaigns: List[Dict[str, Any]], total_budget: float) -> Dict[int, float]:
        """Optimize budget allocation across multiple campaigns"""
        
        # Calculate efficiency score for each campaign
        campaign_scores = []
        for campaign in campaigns:
            roas = campaign.get('roas', 0)
            conversions = campaign.get('conversions', 0)
            cost = campaign.get('cost', 1)
            
            # Efficiency score (weighted combination of ROAS and conversion rate)
            efficiency = (roas * 0.7) + (conversions / cost * 0.3)
            campaign_scores.append({
                'campaign_id': campaign['id'],
                'efficiency': efficiency,
                'min_budget': campaign.get('min_budget', 10),
                'max_budget': campaign.get('max_budget', 1000)
            })
        
        # Sort by efficiency
        campaign_scores.sort(key=lambda x: x['efficiency'], reverse=True)
        
        # Allocate budget proportionally to efficiency
        total_efficiency = sum(c['efficiency'] for c in campaign_scores)
        allocations = {}
        
        for campaign in campaign_scores:
            if total_efficiency > 0:
                allocation = (campaign['efficiency'] / total_efficiency) * total_budget
                # Clamp to min/max
                allocation = max(campaign['min_budget'], min(campaign['max_budget'], allocation))
                allocations[campaign['campaign_id']] = round(allocation, 2)
            else:
                # Equal distribution if no efficiency data
                allocations[campaign['campaign_id']] = round(total_budget / len(campaigns), 2)
        
        return allocations


# Global optimizer instance
campaign_optimizer = CampaignOptimizer()
budget_optimizer = BudgetOptimizer()
