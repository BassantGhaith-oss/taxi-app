elif page == "Visualization":
    st.info("Model Visualization — Monte Carlo Simulation")

    if data.empty:
        st.warning("Dataset not loaded! Please load 'small_data.csv' first to see the plots.")
    else:
        df = data.copy()

        # ---------- Monte Carlo Plot (Plotly) ----------
        N_PATHS = st.slider("Number of Simulated Paths", min_value=50, max_value=500, value=200, step=50)
        max_distance = st.number_input("Max Distance (km)", min_value=1, max_value=500, value=100)
        distances = np.linspace(0, max_distance, 100)
        paths = [np.cumsum(np.random.rand(len(distances))*0.5) for _ in range(N_PATHS)]
        final_fares = [path[-1] for path in paths]
        paths_array = np.array(paths)
        mean_path = np.mean(paths_array, axis=0)
        p10_path = np.percentile(paths_array, 10, axis=0)
        p25_path = np.percentile(paths_array, 25, axis=0)
        p75_path = np.percentile(paths_array, 75, axis=0)
        p90_path = np.percentile(paths_array, 90, axis=0)

        def fare_to_color(fare):
            norm = min(fare / max(final_fares), 1.0)
            return f'rgba(0, {int(200*norm)}, 255, 0.3)'

        fig_mc = go.Figure()
        for i in range(N_PATHS):
            fig_mc.add_trace(go.Scatter(x=distances, y=paths[i], mode='lines',
                                        line=dict(width=0.5, color=fare_to_color(final_fares[i])),
                                        showlegend=False, hoverinfo='skip'))
        # Percentile bands
        fig_mc.add_trace(go.Scatter(
            x=np.concatenate([distances, distances[::-1]]),
            y=np.concatenate([p90_path, p10_path[::-1]]),
            fill='toself', fillcolor='rgba(0,200,255,0.07)',
            line=dict(color='rgba(0,0,0,0)'), name='P10–P90 Band'
        ))
        fig_mc.add_trace(go.Scatter(
            x=np.concatenate([distances, distances[::-1]]),
            y=np.concatenate([p75_path, p25_path[::-1]]),
            fill='toself', fillcolor='rgba(0,200,255,0.12)',
            line=dict(color='rgba(0,0,0,0)'), name='P25–P75 Band'
        ))
        fig_mc.add_trace(go.Scatter(
            x=distances, y=mean_path, mode='lines',
            line=dict(color='#FFE135', width=3.5),
            name=f'Mean Fare (${mean_path[-1]:.2f} at {max_distance}km)'
        ))
        st.plotly_chart(fig_mc, use_container_width=True)

        # ---------- Matplotlib Scatter Plots ----------
        plt.style.use('dark_background')

        # Scatter 1: Trip Distance vs Fare
        fig1, ax1 = plt.subplots(figsize=(8,5))
        ax1.scatter(df['trip_distance'], df['fare_amount'], alpha=0.5, color='#8A2BE2')
        ax1.set_title("Trip Distance vs Fare Amount", color='white')
        ax1.set_xlabel("Trip Distance", color='white')
        ax1.set_ylabel("Fare Amount", color='white')
        ax1.tick_params(axis='x', colors='white')
        ax1.tick_params(axis='y', colors='white')
        st.pyplot(fig1)

        # Scatter 2: Trip Duration vs Fare
        fig2, ax2 = plt.subplots(figsize=(8,5))
        ax2.scatter(df['trip_duration'], df['fare_amount'], alpha=0.5, color='#008080')
        ax2.set_title("Trip Duration vs Fare Amount", color='white')
        ax2.set_xlabel("Trip Duration", color='white')
        ax2.set_ylabel("Fare Amount", color='white')
        ax2.tick_params(axis='x', colors='white')
        ax2.tick_params(axis='y', colors='white')
        st.pyplot(fig2)

        # Histogram 3: Fare Distribution
        bins = [0, 5, 10, 15, 20, 25, 30, 40, 50, 75, 200]
        labels = ['$0–5','$5–10','$10–15','$15–20','$20–25','$25–30','$30–40','$40–50','$50–75','$75+']
        df['fare_bucket'] = pd.cut(df['fare_amount'], bins=bins, labels=labels, include_lowest=True)
        bucket_counts = df['fare_bucket'].value_counts().sort_index()
        fig3, ax3 = plt.subplots(figsize=(8,5))
        ax3.bar(labels, bucket_counts, color='#008080', alpha=0.7)
        ax3.set_title("Fare Distribution Histogram", color='white')
        ax3.set_xlabel("Fare Range ($)", color='white')
        ax3.set_ylabel("Number of Rides", color='white')
        ax3.tick_params(axis='x', rotation=45, colors='white')
        ax3.tick_params(axis='y', colors='white')
        st.pyplot(fig3)

        # Map 4: Pickup Locations with Fare (Plotly)
        fig4 = px.scatter_mapbox(
            df.sample(min(5000,len(df)), random_state=42),
            lat='pickup_latitude',
            lon='pickup_longitude',
            color='fare_amount',
            size='fare_amount',
            color_continuous_scale=px.colors.sequential.Viridis,
            size_max=8,
            opacity=0.7,
            zoom=10,
            mapbox_style='carto-darkmatter'
        )
        fig4.update_layout(paper_bgcolor='black', plot_bgcolor='black', font_color='white')
        st.plotly_chart(fig4, use_container_width=True)
